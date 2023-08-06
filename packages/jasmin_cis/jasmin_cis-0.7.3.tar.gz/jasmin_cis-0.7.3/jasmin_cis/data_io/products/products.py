import logging

import iris
import iris.exceptions

# add includes for plugin finder
from jasmin_cis.data_io.products.abstract_NetCDF_CF import abstract_NetCDF_CF


from jasmin_cis.data_io.hdf_vd import get_data, VDS
from jasmin_cis.data_io.netcdf import get_netcdf_file_variables, remove_variables_with_non_spatiotemporal_dimensions
from jasmin_cis.exceptions import InvalidVariableError, CoordinateNotFoundError
from jasmin_cis.data_io.Coord import Coord, CoordList
from jasmin_cis.data_io.products.AProduct import AProduct
from jasmin_cis.data_io.ungridded_data import UngriddedData, Metadata, UngriddedCoordinates
import jasmin_cis.data_io.gridded_data as gridded_data
import jasmin_cis.utils as utils
import jasmin_cis.data_io.hdf as hdf


class CloudSat(AProduct):

    def get_file_signature(self):
        return [r'.*_CS_.*GRANULE.*\.hdf']

    def get_variable_names(self, filenames, data_type=None):
        from pyhdf.HDF import HDF
        from pyhdf.SD import SD

        valid_variables = set([])
        for filename in filenames:
            # Do VD variables
            datafile = HDF(filename)
            vdata = datafile.vstart()
            variables = vdata.vdatainfo()
            # Assumes that latitude shape == longitude shape (it should):
            dim_length = [var[3] for var in variables if var[0] == 'Latitude'][0]
            for var in variables:
                if var[3] == dim_length:
                    valid_variables.add(var[0])

            # Do SD variables:
            sd = SD(filename)
            datasets = sd.datasets()
            if 'Height' in datasets:
                valid_shape = datasets['Height'][1]
                for var in datasets:
                    if datasets[var][1] == valid_shape:
                        valid_variables.add(var)

        return valid_variables

    def _generate_time_array(self, vdata):
        import jasmin_cis.data_io.hdf_vd as hdf_vd
        import datetime as dt
        from jasmin_cis.time_util import convert_sec_since_to_std_time_array

        Cloudsat_start_time = dt.datetime(1993,1,1,0,0,0)

        arrays = []
        for i,j in zip(vdata['Profile_time'],vdata['TAI_start']):
            time = hdf_vd.get_data(i)
            start = hdf_vd.get_data(j)
            time += start
            # Do the conversion to standard time here before we expand the time array...
            time = convert_sec_since_to_std_time_array(time, Cloudsat_start_time)
            arrays.append(time)
        return utils.concatenate(arrays)

    def _create_coord_list(self, filenames):
        from jasmin_cis.time_util import cis_standard_time_unit
        # list of coordinate variables we are interested in
        variables = ['Latitude', 'Longitude', 'TAI_start', 'Profile_time', 'Height']

        # reading the various files
        try:
            logging.info("Listing coordinates: " + str(variables))
            sdata, vdata = hdf.read(filenames, variables)

            # altitude coordinate
            height = sdata['Height']
            height_data = hdf.read_data(height, "SD")
            height_metadata = hdf.read_metadata(height, "SD")
            height_coord = Coord(height_data, height_metadata, "Y")

        except InvalidVariableError:
            # This means we are reading a Cloudsat file without height, so remove height from the variables list
            variables.remove('Height')
            logging.info("Listing coordinates: " + str(variables))
            sdata, vdata = hdf.read(filenames, variables)

            height_data = None
            height_coord = None

        # latitude
        lat = vdata['Latitude']
        lat_data = hdf.read_data(lat, "VD")
        if height_data is not None:
            lat_data = utils.expand_1d_to_2d_array(lat_data, len(height_data[0]), axis=1)
        lat_metadata = hdf.read_metadata(lat,"VD")
        lat_metadata.shape = lat_data.shape
        lat_coord = Coord(lat_data, lat_metadata)

        # longitude
        lon = vdata['Longitude']
        lon_data = hdf.read_data(lon, "VD")
        if height_data is not None:
            lon_data = utils.expand_1d_to_2d_array(lon_data, len(height_data[0]), axis=1)
        lon_metadata = hdf.read_metadata(lon, "VD")
        lon_metadata.shape = lon_data.shape
        lon_coord = Coord(lon_data, lon_metadata)

        # time coordinate
        time_data = self._generate_time_array(vdata)
        if height_data is not None:
            time_data = utils.expand_1d_to_2d_array(time_data, len(height_data[0]), axis=1)
        time_coord = Coord(time_data,Metadata(name='Profile_time', standard_name='time', shape=time_data.shape,
                                              units=str(cis_standard_time_unit),
                                              calendar=cis_standard_time_unit.calendar),"X")


        # create object containing list of coordinates
        coords = CoordList()
        coords.append(lat_coord)
        coords.append(lon_coord)
        if height_coord is not None:
            coords.append(height_coord)
        coords.append(time_coord)

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):

        logging.debug("Creating data object for variable " + variable)

        # reading coordinates
        coords = self._create_coord_list(filenames)

        # reading of variables
        sdata, vdata = hdf.read(filenames, variable)

        #missing values
        missing_values = [0,-9999,-4444,-3333]

        # retrieve data + its metadata
        if variable in vdata:
            # vdata should be expanded in the same way as the coordinates are expanded
            try:
                height_length = coords.get_coord('Height').shape[1]
                var = utils.expand_1d_to_2d_array(hdf.read_data(vdata[variable], "VD", missing_values),
                                                  height_length, axis=1)
            except CoordinateNotFoundError:
                var = hdf.read_data(vdata[variable], "VD", missing_values)
            metadata = hdf.read_metadata(vdata[variable],"VD")
        elif variable in sdata:
            var = hdf.read_data(sdata[variable], "SD",missing_values)
            metadata = hdf.read_metadata(sdata[variable],"SD")
        else:
            raise ValueError("variable not found")

        return UngriddedData(var,metadata,coords)


class MODIS_L3(AProduct):

    def _parse_datetime(self,metadata_dict,keyword):
        import re
        res = ""
        for s in metadata_dict.itervalues():
            i_start = s.find(keyword)
            ssub = s[i_start:len(s)]
            i_end = ssub.find("END_OBJECT")
            ssubsub = s[i_start:i_start+i_end]
            matches = re.findall('".*"',ssubsub)
            if len(matches) > 0:
                res = matches[0].replace('\"','')
                if res is not "":
                    break
        return res

    def _get_start_date(self, filename):
        from jasmin_cis.time_util import parse_datetimestr_to_std_time
        metadata_dict = hdf.get_hdf4_file_metadata(filename)
        date = self._parse_datetime(metadata_dict,'RANGEBEGINNINGDATE')
        time = self._parse_datetime(metadata_dict,'RANGEBEGINNINGTIME')
        datetime_str = date + " " + time
        return parse_datetimestr_to_std_time(datetime_str)

    def _get_end_date(self, filename):
        from jasmin_cis.time_util import parse_datetimestr_to_std_time
        metadata_dict = hdf.get_hdf4_file_metadata(filename)
        date = self._parse_datetime(metadata_dict,'RANGEENDINGDATE')
        time = self._parse_datetime(metadata_dict,'RANGEENDINGTIME')
        datetime_str = date + " " + time
        return parse_datetimestr_to_std_time(datetime_str)

    def get_file_signature(self):
        product_names = ['MYD08_D3','MOD08_D3',"MOD08_E3"]
        regex_list = [ r'.*' + product + '.*\.hdf' for product in product_names]
        return regex_list

    def get_variable_names(self, filenames, data_type=None):
        import pyhdf.SD

        variables = set([])
        for filename in filenames:
            sd = pyhdf.SD.SD(filename)
            for var_name, var_info in sd.datasets().iteritems():
                # Check that the dimensions are correct
                if var_info[0] == ('YDim:mod08', 'XDim:mod08'):
                    variables.add(var_name)

        return variables

    def _create_coord_list(self, filenames):
        import numpy as np
        from jasmin_cis.time_util import calculate_mid_time, cis_standard_time_unit

        variables = ['XDim','YDim']
        logging.info("Listing coordinates: " + str(variables))

        sdata, vdata = hdf.read(filenames,variables)

        lat = sdata['YDim']
        lat_metadata = hdf.read_metadata(lat, "SD")

        lon = sdata['XDim']
        lon_metadata = hdf.read_metadata(lon, "SD")

        # expand lat and lon data array so that they have the same shape
        lat_data = utils.expand_1d_to_2d_array(hdf.read_data(lat,"SD"),lon_metadata.shape,axis=1) # expand latitude column wise
        lon_data = utils.expand_1d_to_2d_array(hdf.read_data(lon,"SD"),lat_metadata.shape,axis=0) # expand longitude row wise

        lat_metadata.shape = lat_data.shape
        lon_metadata.shape = lon_data.shape

        # to make sure "Latitude" and "Longitude", i.e. the standard_name is displayed instead of "YDim"and "XDim"
        lat_metadata.standard_name = "latitude"
        lat_metadata._name = ""
        lon_metadata.standard_name = "longitude"
        lon_metadata._name = ""

        # create arrays for time coordinate using the midpoint of the time delta between the start date and the end date
        time_data_array = []
        for filename in filenames:
            mid_datetime = calculate_mid_time(self._get_start_date(filename),self._get_end_date(filename))
            logging.debug("Using "+str(mid_datetime)+" as datetime for file "+str(filename))
            # Only use part of the full lat shape as it has already been concattenated
            time_data = np.empty((lat_metadata.shape[0]/len(filenames),lat_metadata.shape[1]),dtype='float64')
            time_data.fill(mid_datetime)
            time_data_array.append(time_data)
        time_data = utils.concatenate(time_data_array)
        time_metadata = Metadata(name='Date Time', standard_name='time', shape=time_data.shape,
                                 units=str(cis_standard_time_unit),calendar=cis_standard_time_unit.calendar)

        coords = CoordList()
        coords.append(Coord(lon_data, lon_metadata,'X'))
        coords.append(Coord(lat_data, lat_metadata,'Y'))
        coords.append(Coord(time_data, time_metadata,'T'))

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):

        logging.debug("Creating data object for variable " + variable)

        # reading coordinates
        # the variable here is needed to work out whether to apply interpolation to the lat/lon data or not
        coords = self._create_coord_list(filenames)

        # reading of variables
        sdata, vdata = hdf.read(filenames, variable)

        # retrieve data + its metadata
        var = sdata[variable]
        metadata = hdf.read_metadata(var, "SD")

        data = UngriddedData(var, metadata, coords)
        return data

class MODIS_L2(AProduct):

    modis_scaling = ["1km","5km","10km"]

    def get_file_signature(self):
        product_names = ['MYD06_L2','MOD06_L2','MYD04_L2','MOD04_L2']
        regex_list = [ r'.*' + product + '.*\.hdf' for product in product_names]
        return regex_list

    def get_variable_names(self, filenames, data_type=None):
        import pyhdf.SD

        # Determine the valid shape for variables
        sd = pyhdf.SD.SD(filenames[0])
        datasets = sd.datasets()
        valid_shape = datasets['Latitude'][1]  # Assumes that latitude shape == longitude shape (it should)

        variables = set([])
        for filename in filenames:
            sd = pyhdf.SD.SD(filename)
            for var_name, var_info in sd.datasets().iteritems():
                if var_info[1] == valid_shape:
                    variables.add(var_name)

        return variables

    def __get_data_scale(self, filename, variable):
        from jasmin_cis.exceptions import InvalidVariableError
        from pyhdf import SD

        try:
            meta = SD.SD(filename).datasets()[variable][0][0]
        except KeyError:
            raise InvalidVariableError("Variable "+variable+" not found")

        for scaling in self.modis_scaling:
            if scaling in meta:
                return scaling
        return None

    def __field_interpolate(self,data,factor=5):
        '''
        Interpolates the given 2D field by the factor,
        edge pixels are defined by the ones in the centre,
        odd factords only!
        '''
        import numpy as np

        logging.debug("Performing interpolation...")

        output = np.zeros((factor*data.shape[0],factor*data.shape[1]))*np.nan
        output[int(factor/2)::factor,int(factor/2)::factor] = data
        for i in range(1,factor+1):
            output[(int(factor/2)+i):(-1*factor/2+1):factor,:] = i*((output[int(factor/2)+factor::factor,:]-output[int(factor/2):(-1*factor):factor,:])
                                                                    /float(factor))+output[int(factor/2):(-1*factor):factor,:]
        for i in range(1,factor+1):
            output[:,(int(factor/2)+i):(-1*factor/2+1):factor] = i*((output[:,int(factor/2)+factor::factor]-output[:,int(factor/2):(-1*factor):factor])
                                                                    /float(factor))+output[:,int(factor/2):(-1*factor):factor]
        return output

    def _create_coord_list(self, filenames, variable=None):
        import datetime as dt

        variables = [ 'Latitude','Longitude','Scan_Start_Time']
        logging.info("Listing coordinates: " + str(variables))

        sdata, vdata = hdf.read(filenames,variables)

        apply_interpolation = False
        if variable is not None:
            scale = self.__get_data_scale(filenames[0], variable)
            apply_interpolation = True if scale is "1km" else False

        lat = sdata['Latitude']
        lat_data = self.__field_interpolate(hdf.read_data(lat,"SD")) if apply_interpolation else hdf.read_data(lat,"SD")
        lat_metadata = hdf.read_metadata(lat, "SD")
        lat_coord = Coord(lat_data, lat_metadata,'Y')

        lon = sdata['Longitude']
        lon_data = self.__field_interpolate(hdf.read_data(lon,"SD")) if apply_interpolation else hdf.read_data(lon,"SD")
        lon_metadata = hdf.read_metadata(lon,"SD")
        lon_coord = Coord(lon_data, lon_metadata,'X')

        time = sdata['Scan_Start_Time']
        time_metadata = hdf.read_metadata(time,"SD")
        # Ensure the standard name is set
        time_metadata.standard_name = 'time'
        time_coord = Coord(time,time_metadata,"T")
        time_coord.convert_TAI_time_to_std_time(dt.datetime(1993,1,1,0,0,0))

        return CoordList([lat_coord,lon_coord,time_coord])

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        logging.debug("Creating data object for variable " + variable)

        # reading coordinates
        # the variable here is needed to work out whether to apply interpolation to the lat/lon data or not
        coords = self._create_coord_list(filenames, variable)

        # reading of variables
        sdata, vdata = hdf.read(filenames, variable)

        # retrieve data + its metadata
        var = sdata[variable]
        metadata = hdf.read_metadata(var, "SD")

        return UngriddedData(var, metadata, coords)

class Cloud_CCI(AProduct):

    def get_file_signature(self):
        return [r'..*ESACCI.*CLOUD.*']

    def _create_coord_list(self, filenames):

        from jasmin_cis.data_io.netcdf import read_many_files_individually, get_metadata
        from jasmin_cis.data_io.Coord import Coord

        variables = ["lat", "lon", "time"]
        logging.info("Listing coordinates: " + str(variables))

        var_data = read_many_files_individually(filenames, variables)

        coords = CoordList()
        coords.append(Coord(var_data['lat'], get_metadata(var_data['lat'][0]), 'Y'))
        coords.append(Coord(var_data['lon'], get_metadata(var_data['lon'][0]),'X'))
        time_coord = Coord(var_data['time'], get_metadata(var_data['time'][0]))

        # TODO: Is this really julian?
        time_coord.convert_julian_to_std_time()
        coords.append(time_coord)

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):

        from jasmin_cis.data_io.netcdf import get_metadata, read_many_files_individually

        coords = self._create_coord_list(filenames)
        var = read_many_files_individually(filenames, [variable])
        metadata = get_metadata(var[variable][0])

        return UngriddedData(var[variable], metadata, coords)


class Aerosol_CCI(AProduct):

    valid_dimensions = ["pixel_number"]

    def get_file_signature(self):
        return [r'.*ESACCI.*AEROSOL.*']

    def _create_coord_list(self, filenames):

        from jasmin_cis.data_io.netcdf import read_many_files, get_metadata
        from jasmin_cis.data_io.Coord import Coord
        import datetime

        #!FIXME: when reading an existing file variables might be "latitude", "longitude"
        variables = ["lat", "lon", "time"]
        logging.info("Listing coordinates: " + str(variables))

        data = read_many_files(filenames, variables, dim="pixel_number")

        coords = CoordList()
        coords.append(Coord(data["lon"], get_metadata(data["lon"]), "X"))
        coords.append(Coord(data["lat"], get_metadata(data["lat"]), "Y"))
        time_coord = Coord(data["time"], get_metadata(data["time"]), "T")
        time_coord.convert_TAI_time_to_std_time(datetime.datetime(1970,1,1))
        coords.append(time_coord)

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        from jasmin_cis.data_io.netcdf import read_many_files, get_metadata

        coords = self._create_coord_list(filenames)
        data = read_many_files(filenames, variable, dim="pixel_number")
        metadata = get_metadata(data[variable])

        return UngriddedData(data[variable], metadata, coords)


class abstract_Caliop(AProduct):

    def get_file_signature(self):
        '''
        To be implemented by subclcass
        :return:
        '''
        return []

    def get_variable_names(self, filenames, data_type=None):
        import pyhdf.SD
        import pyhdf.HDF
        variables = set([])

        # Determine the valid shape for variables
        sd = pyhdf.SD.SD(filenames[0])
        datasets = sd.datasets()
        len_x = datasets['Latitude'][1][0]  # Assumes that latitude shape == longitude shape (it should)
        alt_data = get_data(VDS(filenames[0], "Lidar_Data_Altitudes"), True)
        len_y = alt_data.shape[0]
        valid_shape = (len_x, len_y)

        for filename in filenames:
            sd = pyhdf.SD.SD(filename)
            for var_name, var_info in sd.datasets().iteritems():
                if var_info[1] == valid_shape:
                    variables.add(var_name)

        return variables

    def _create_coord_list(self, filenames, index_offset=0):
        from jasmin_cis.data_io.hdf_vd import get_data
        from jasmin_cis.data_io.hdf_vd import VDS
        from pyhdf.error import HDF4Error
        from jasmin_cis.data_io import hdf_sd
        import datetime as dt
        from jasmin_cis.time_util import convert_sec_since_to_std_time_array, cis_standard_time_unit

        variables = ['Latitude','Longitude', "Profile_Time", "Pressure"]
        logging.info("Listing coordinates: " + str(variables))

        # reading data from files
        sdata = {}
        for filename in filenames:
            try:
                sds_dict = hdf_sd.read(filename, variables)
            except HDF4Error as e:
                raise IOError(str(e))

            for var in sds_dict.keys():
                utils.add_element_to_list_in_dict(sdata, var, sds_dict[var])

        alt_name = "altitude"
        logging.info("Additional coordinates: '" + alt_name + "'")

        # work out size of data arrays
        # the coordinate variables will be reshaped to match that.
        # NOTE: This assumes that all Caliop_L1 files have the same altitudes.
        #       If this is not the case, then the following line will need to be changed
        #       to concatenate the data from all the files and not just arbitrarily pick
        #       the altitudes from the first file.
        alt_data = get_data(VDS(filenames[0],"Lidar_Data_Altitudes"), True)
        alt_data *= 1000.0  # Convert to m
        len_x = alt_data.shape[0]

        lat_data = hdf.read_data(sdata['Latitude'],"SD")
        len_y = lat_data.shape[0]

        new_shape = (len_x, len_y)

        # altitude
        alt_data = utils.expand_1d_to_2d_array(alt_data,len_y,axis=0)
        alt_metadata = Metadata(name=alt_name, standard_name=alt_name, shape=new_shape)
        alt_coord = Coord(alt_data,alt_metadata)

        # pressure
        pres_data = hdf.read_data(sdata['Pressure'],"SD")
        pres_metadata = hdf.read_metadata(sdata['Pressure'], "SD")
        pres_metadata.shape = new_shape
        pres_coord = Coord(pres_data, pres_metadata, 'P')

        # latitude
        lat_data = utils.expand_1d_to_2d_array(lat_data[:,index_offset],len_x,axis=1)
        lat_metadata = hdf.read_metadata(sdata['Latitude'], "SD")
        lat_metadata.shape = new_shape
        lat_coord = Coord(lat_data, lat_metadata, 'Y')

        # longitude
        lon = sdata['Longitude']
        lon_data = hdf.read_data(lon,"SD")
        lon_data = utils.expand_1d_to_2d_array(lon_data[:,index_offset],len_x,axis=1)
        lon_metadata = hdf.read_metadata(lon,"SD")
        lon_metadata.shape = new_shape
        lon_coord = Coord(lon_data, lon_metadata,'X')

        #profile time, x
        time = sdata['Profile_Time']
        time_data = hdf.read_data(time,"SD")
        time_data = convert_sec_since_to_std_time_array(time_data, dt.datetime(1993,1,1,0,0,0))
        time_data = utils.expand_1d_to_2d_array(time_data[:,index_offset],len_x,axis=1)
        time_coord = Coord(time_data,Metadata(name='Profile_Time', standard_name='time', shape=time_data.shape,
                                              units=str(cis_standard_time_unit),
                                              calendar=cis_standard_time_unit.calendar),"T")

        # create the object containing all coordinates
        coords = CoordList()
        coords.append(lat_coord)
        coords.append(lon_coord)
        coords.append(time_coord)
        coords.append(alt_coord)
        if pres_data.shape == alt_data.shape:
            # For MODIS L1 this may is not be true, so skips the air pressure reading. If required for MODIS L1 then
            # some kind of interpolation of the air pressure would be required, as it is on a different (smaller) grid
            # than for the Lidar_Data_Altitudes.
            coords.append(pres_coord)

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        '''
        To be implemented by subclass
        :param filenames:
        :param variable:
        :return:
        '''
        return None

    def get_calipso_data(self, sds):
        """
        Reads raw data from an SD instance. Automatically applies the
        scaling factors and offsets to the data arrays found in Calipso data.

        Returns:
            A numpy array containing the raw data with missing data is replaced by NaN.

        Arguments:
            sds        -- The specific sds instance to read

        """
        from jasmin_cis.utils import create_masked_array_for_missing_data

        calipso_fill_values = {'Float_32' : -9999.0,
                               #'Int_8' : 'See SDS description',
                               'Int_16' : -9999,
                               'Int_32' : -9999,
                               'UInt_8' : -127,
                               #'UInt_16' : 'See SDS description',
                               #'UInt_32' : 'See SDS description',
                               'ExtinctionQC Fill Value' : 32768,
                               'FeatureFinderQC No Features Found' : 32767,
                               'FeatureFinderQC Fill Value' : 65535}

        data = sds.get()
        attributes = sds.attributes()

        # Missing data.
        missing_val = attributes.get('fillvalue', None)
        if missing_val is None:
            try:
                missing_val = calipso_fill_values[attributes.get('format', None)]
            except KeyError:
                # Last guess
                missing_val = attributes.get('_FillValue', None)

        data = create_masked_array_for_missing_data(data, missing_val)

        # Offsets and scaling.
        offset  = attributes.get('add_offset', 0)
        scale_factor = attributes.get('scale_factor', 1)
        data = self.apply_scaling_factor_CALIPSO(data, scale_factor, offset)

        return data

    def apply_scaling_factor_CALIPSO(self,data, scale_factor, offset):
        '''
        Apply scaling factor Calipso data
        :param data:
        :param scale_factor:
        :param offset:
        :return:
        '''
        return (data/scale_factor) + offset


class Caliop_L2(abstract_Caliop):

    def get_file_signature(self):
        return [r'CAL_LID_L2_05kmAPro-Prov-V3.*hdf']

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(super(Caliop_L2, self)._create_coord_list(filenames, index_offset=1))

    def create_data_object(self, filenames, variable):
        logging.debug("Creating data object for variable " + variable)

        # reading coordinates
        # the variable here is needed to work out whether to apply interpolation to the lat/lon data or not
        coords = self._create_coord_list(filenames)

        # reading of variables
        sdata, vdata = hdf.read(filenames, variable)

        # retrieve data + its metadata
        var = sdata[variable]
        metadata = hdf.read_metadata(var, "SD")

        return UngriddedData(var, metadata, coords, self.get_calipso_data)


class Caliop_L1(abstract_Caliop):

    def get_file_signature(self):
        return [r'CAL_LID_L1-ValStage1-V3.*hdf']

    def offset(self):
        return 0

    def create_data_object(self, filenames, variable):
        logging.debug("Creating data object for variable " + variable)

        # reading coordinates
        # the variable here is needed to work out whether to apply interpolation to the lat/lon data or not
        coords = self._create_coord_list(filenames)

        # reading of variables
        sdata, vdata = hdf.read(filenames, variable)

        # retrieve data + its metadata
        var = sdata[variable]
        metadata = hdf.read_metadata(var, "SD")

        return UngriddedData(var, metadata, coords, self.get_calipso_data)


class cis(AProduct):

    # If a file matches the CIS product signature as well as another signature (e.g. because we aggregated from another
    # data product) we need to prioritise the CIS data product
    priority = 100

    def get_file_signature(self):
        return [r'cis\-.*\.nc']

    def create_coords(self, filenames, usr_variable=None):
        from jasmin_cis.data_io.netcdf import read_many_files_individually, get_metadata
        from jasmin_cis.data_io.Coord import Coord
        from jasmin_cis.exceptions import InvalidVariableError

        variables = [("longitude", "x"), ("latitude", "y"), ("altitude", "z"), ("time", "t"), ("air_pressure", "p")]

        logging.info("Listing coordinates: " + str(variables))

        coords = CoordList()
        for variable in variables:
            try:
                var_data = read_many_files_individually(filenames,variable[0])[variable[0]]
                coords.append(Coord(var_data, get_metadata(var_data[0]),axis=variable[1]))
            except InvalidVariableError:
                pass

        # Note - We don't need to convert this time coord as it should have been written in our
        #  'standard' time unit

        if usr_variable is None:
            res = UngriddedCoordinates(coords)
        else:
            usr_var_data = read_many_files_individually(filenames,usr_variable)[usr_variable]
            res = UngriddedData(usr_var_data, get_metadata(usr_var_data[0]), coords)

        return res

    def create_data_object(self, filenames, variable):
        return self.create_coords(filenames, variable)


class abstract_NetCDF_CF_Gridded(abstract_NetCDF_CF):

    def get_file_signature(self):
        # We don't know of any 'standard' netCDF CF model data yet...
        return []

    def get_variable_names(self, filenames, data_type=None):
        variables = []
        for filename in filenames:
            file_variables = get_netcdf_file_variables(filename, exclude_coords=True)
            remove_variables_with_non_spatiotemporal_dimensions(file_variables, ['lat', 'lon', 'time',
                                                                                 'altitude', 'pressure'])
            variables.extend(file_variables)
        return set(variables)

    def create_coords(self, filenames, variable=None):
        """Reads the coordinates on which a variable depends.
        Note: This calls create_data_object because the coordinates are returned as a Cube.
        :param filenames: list of names of files from which to read coordinates
        :param variable: name of variable for which the coordinates are required
                         (optional if file contains only one cube)
        :return: iris.cube.Cube
        """
        return self._create_cube(filenames, variable, False)

    def create_data_object(self, filenames, variable):
        """

        :param filenames: List of filenames to read coordinates from
        :param variable: Optional variable to read while we're reading the coordinates, can be a string or a VariableConstraint object
        :return: If variable was specified this will return an UngriddedData object, otherwise a CoordList
        """
        return self._create_cube(filenames, variable, True)

    def _create_cube(self, filenames, variable, remove_length_one_dimensions):
        """Creates a cube for the specified variable.
        :param filenames: List of filenames to read coordinates from
        :param variable: Optional variable to read while we're reading the coordinates, can be a string or a VariableConstraint object
        :return: If variable was specified this will return an UngriddedData object, otherwise a CoordList
        """
        from jasmin_cis.exceptions import InvalidVariableError

        # Check if the files given actually exist.
        for filename in filenames:
            with open(filename) as f: pass

        try:
            cube = gridded_data.load_cube(filenames, variable)
        except iris.exceptions.ConstraintMismatchError:
            raise InvalidVariableError("Variable not found: " + str(variable) +
                                       "\nTo see a list of variables run: cis info " + filenames[0])
        except ValueError as e:
            raise IOError(e)

        # Fix to create a hybrid pressure factory in Iris. More attempts may be required for different file types. This
        # should be removed once the relevant Iris issue is resolved https://github.com/SciTools/iris/issues/933.
        try:
            cube.add_aux_factory(iris.aux_factory.HybridPressureFactory(
                cube.coord(var_name="hyam"), cube.coord(var_name="hybm"), cube.coord(var_name="PS")))
        except iris.exceptions.CoordinateNotFoundError:
            pass

        sub_cube = list(cube.slices([ coord for coord in cube.coords(dim_coords=True) if coord.points.size > 1]))[0]
        #  Ensure that there are no extra dimensions which can confuse the plotting.
        # E.g. the shape of the cube might be (1, 145, 165) and so we don't need to know about
        #  the dimension whose length is one. The above list comprehension would return a cube of
        #  shape (145, 165)

        return sub_cube


class DisplayConstraint(iris.Constraint):
    """Variant of iris.Constraint with a string value that can be displayed.
    """
    def __init__(self, *args, **kwargs):
        sc_kwargs = kwargs.copy()
        self.display = str(sc_kwargs.get('display', None))
        if self.display is not None:
            del sc_kwargs['display']
        super(DisplayConstraint, self).__init__(*args, **sc_kwargs)

    def __str__(self):
        if self.display is not None:
            return self.display
        else:
            return super(DisplayConstraint, self).__str__()


class NetCDF_Gridded(abstract_NetCDF_CF_Gridded):
    """Reads gridded netCDF identifying variable by variable name.
    """
    def get_file_signature(self):
        # Generic product class so no signature.
        return []

    def create_coords(self, filenames, variable=None):
        """Reads the coordinates on which a variable depends.
        Note: This calls create_data_object because the coordinates are returned as a Cube.
        :param filenames: list of names of files from which to read coordinates
        :param variable: name of variable for which the coordinates are required
                         (optional if file contains only one cube)
        :return: iris.cube.Cube
        """

        return self.create_data_object(filenames, variable)

    def create_data_object(self, filenames, variable):
        """Reads the data for a variable.
        :param filenames: list of names of files from which to read data
        :param variable: (optional) name of variable; if None, the file(s) must contain data for only one cube
        :return: iris.cube.Cube
        """
        from jasmin_cis.time_util import convert_cube_time_coord_to_standard_time

        variable_constraint = None
        if variable is not None:
            variable_constraint = DisplayConstraint(cube_func=(lambda c: c.var_name == variable or
                                                                         c.standard_name == variable or
                                                                         c.long_name == variable), display=variable)
        cube = super(NetCDF_Gridded, self).create_data_object(filenames, variable_constraint)

        try:
            cube = convert_cube_time_coord_to_standard_time(cube)
        except iris.exceptions.CoordinateNotFoundError:
            pass
        return cube


class Aeronet(AProduct):

    def get_file_signature(self):
        return [r'.*\.lev20']

    def _create_coord_list(self, filenames, data = None):
        from jasmin_cis.data_io.ungridded_data import Metadata
        from jasmin_cis.data_io.aeronet import load_multiple_aeronet

        if data is None:
            data = load_multiple_aeronet(filenames)

        coords = CoordList()
        coords.append(Coord(data['longitude'], Metadata(name="Longitude", shape=(len(data),), units="degrees_east", range=(-180,180))))
        coords.append(Coord(data['latitude'], Metadata(name="Latitude", shape=(len(data),), units="degrees_north", range=(-90,90))))
        coords.append(Coord(data['altitude'], Metadata(name="Altitude", shape=(len(data),), units="meters", range=(-90,90))))
        time_coord = Coord(data["datetime"], Metadata(name="DateTime",standard_name='time', shape=(len(data),), units="DateTime Object"), "X")
        time_coord.convert_datetime_to_standard_time()
        coords.append(time_coord)

        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        from jasmin_cis.data_io.aeronet import load_multiple_aeronet
        from jasmin_cis.exceptions import InvalidVariableError

        try:
            data_obj = load_multiple_aeronet(filenames, [variable])
        except ValueError:
            raise InvalidVariableError(variable + " does not exist in " + str(filenames))

        coords = self._create_coord_list(filenames, data_obj)

        return UngriddedData(data_obj[variable],
                             Metadata(name=variable, long_name=variable, shape=(len(data_obj),), missing_value=-999.0),
                             coords)


class ASCII_Hyperpoints(AProduct):

    def get_file_signature(self):
        return [r'.*\.txt']

    def get_variable_names(self, filenames, data_type=None):
        return ['value']

    def create_coords(self, filenames, variable=None):
        from jasmin_cis.data_io.ungridded_data import Metadata
        from numpy import genfromtxt
        from jasmin_cis.exceptions import InvalidVariableError
        from jasmin_cis.time_util import parse_datetimestr_to_std_time_array

        array_list = []

        for filename in filenames:
            try:
                array_list.append(genfromtxt(filename, dtype="f8,f8,f8,S20,f8",
                                             names=['latitude', 'longitude', 'altitude', 'time', 'value'],
                                             delimiter=',', missing_values='', usemask=True, invalid_raise=True))
            except:
                raise IOError('Unable to read file '+filename)

        data_array = utils.concatenate(array_list)
        n_elements = len(data_array['latitude'])

        coords = CoordList()
        coords.append(Coord(data_array["latitude"], Metadata(standard_name="latitude", shape=(n_elements,), units="degrees_north")))
        coords.append(Coord(data_array["longitude"], Metadata(standard_name="longitude", shape=(n_elements,), units="degrees_east")))
        coords.append(Coord(data_array["altitude"], Metadata(standard_name="altitude", shape=(n_elements,), units="meters")))

        time_arr = parse_datetimestr_to_std_time_array(data_array["time"])
        time = Coord(time_arr, Metadata(standard_name="time", shape=(n_elements,), units="days since 1600-01-01 00:00:00"))
        coords.append(time)

        if variable:
            try:
                data = UngriddedData(data_array['value'], Metadata(name="value", shape=(n_elements,), units="unknown"), coords)
            except:
                InvalidVariableError("Value column does not exist in file " + filenames)
            return data
        else:
            return UngriddedCoordinates(coords)

    def create_data_object(self, filenames, variable):
        return self.create_coords(filenames, True)


class default_NetCDF(NetCDF_Gridded):
    """
    This class should always be the last in the sorted list (last alphabetically) - and hence the default for *.nc
    files which have not otherwise been matched.
    """
    def get_file_signature(self):
        return [r'.*\.nc']
