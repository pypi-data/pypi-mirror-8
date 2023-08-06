import __builtin__
import logging

import iris
import numpy as np

from jasmin_cis.col_framework import (Colocator, Constraint, PointConstraint, CellConstraint,
                                      IndexedConstraint, Kernel)
import jasmin_cis.exceptions
from jasmin_cis.data_io.gridded_data import GriddedData, make_from_cube
from jasmin_cis.data_io.hyperpoint import HyperPoint, HyperPointList
from jasmin_cis.data_io.ungridded_data import LazyData, Metadata
import jasmin_cis.data_index as data_index
import jasmin_cis.utils


class GeneralUngriddedColocator(Colocator):

    def __init__(self, fill_value=None, var_name='', var_long_name='', var_units='',
                 missing_data_for_missing_sample=False):
        super(GeneralUngriddedColocator, self).__init__()
        if fill_value is not None:
            try:
                self.fill_value = float(fill_value)
            except ValueError:
                raise jasmin_cis.exceptions.InvalidCommandLineOptionError(
                    'Dummy Constraint fill_value must be a valid float')
        self.var_name = var_name
        self.var_long_name = var_long_name
        self.var_units = var_units
        self.missing_data_for_missing_sample = missing_data_for_missing_sample

    def colocate(self, points, data, constraint, kernel):
        """
        This colocator takes a list of HyperPoints and a data object (currently either Ungridded
        data or a Cube) and returns one new LazyData object with the values as determined by the
        constraint and kernel objects. The metadata for the output LazyData object is copied from
        the input data object.

        :param points: UngriddedData or UngriddedCoordinates defining the sample points
        :param data: An UngriddedData object or Cube, or any other object containing metadata that
                     the constraint object can read
        :param constraint: An instance of a Constraint subclass which takes a data object and
                           returns a subset of that data based on it's internal parameters
        :param kernel: An instance of a Kernel subclass which takes a number of points and returns
                       a single value
        :return: A single LazyData object
        """
        metadata = data.metadata

        # Convert ungridded data to a list of points if kernel needs it.
        # Special case checks for kernels that use a cube - this could be done more elegantly.
        if isinstance(kernel, nn_gridded) or isinstance(kernel, li):
            if not isinstance(data, iris.cube.Cube):
                raise ValueError("Ungridded data cannot be used with kernel nn_gridded or li")
            if constraint is not None and not isinstance(constraint, DummyConstraint):
                raise ValueError("A constraint cannot be specified with kernel nn_gridded or li")
            data_points = data
            _fix_cube_longitude_range(points.coords(), data)
        else:
            data_points = data.get_non_masked_points()
            _fix_longitude_range(points.coords(), data_points)

        # Create index if constraint and/or kernel require one.
        coord_map = None
        data_index.create_indexes(constraint, points, data_points, coord_map)
        data_index.create_indexes(kernel, points, data_points, coord_map)

        logging.info("--> Colocating...")

        sample_points = points.get_all_points()

        # Create output arrays.
        if self.var_name == '':
            self.var_name = data.name()
        if self.var_long_name == '':
            self.var_long_name = metadata.long_name
        if self.var_units == '':
            self.var_units = data.units
        var_set_details = kernel.get_variable_details(self.var_name, self.var_long_name, self.var_units)
        if var_set_details is None:
            var_set_details = ((self.var_name, self.var_long_name, self.var_units),)
        values = np.zeros((len(var_set_details), len(sample_points))) + self.fill_value

        # Apply constraint and/or kernel to each sample point.
        for i, point in sample_points.enumerate_non_masked_points():
            if constraint is None:
                con_points = data_points
            else:
                con_points = constraint.constrain_points(point, data_points)
            try:
                value_obj = kernel.get_value(point, con_points)
                # Kernel returns either a single value or a tuple of values to insert into each output variable.
                if isinstance(value_obj, tuple):
                    for idx, val in enumerate(value_obj):
                        if not np.isnan(val):
                            values[idx, i] = val
                else:
                    values[0, i] = value_obj
            except ValueError:
                pass

        return_data = []
        for idx, var_details in enumerate(var_set_details):
            if idx == 0:
                new_data = LazyData(values[0, :], metadata)
                new_data.metadata._name = var_details[0]
                new_data.metadata.long_name = var_details[1]
                new_data.metadata.shape = (len(sample_points),)
                new_data.metadata.missing_value = self.fill_value
                new_data.units = var_details[2]
            else:
                var_metadata = Metadata(name=var_details[0], long_name=var_details[1], shape=(len(sample_points),),
                                        missing_value=self.fill_value, units=var_details[2])
                new_data = LazyData(values[idx, :], var_metadata)
            return_data.append(new_data)

        return return_data


class DummyColocator(Colocator):

    def colocate(self, points, data, constraint, kernel):
        '''
            This colocator does no colocation at all - it just returns the original data values. This might be useful
            if the input data for one variable is already known to be on the same grid as points. This routine could
            check the coordinates are the same but currently does no such check.
        :param points: A list of HyperPoints
        :param data: An UngriddedData object or Cube
        :param constraint: Unused
        :param kernel: Unused
        :return: A single LazyData object
        '''
        from jasmin_cis.data_io.ungridded_data import LazyData

        logging.info("--> Colocating...")

        new_data = LazyData(data.data, data.metadata)
        return [new_data]


class DummyConstraint(Constraint):

    def constrain_points(self, point, data):
        # This is a null constraint - all of the points just get passed back
        return data


class SepConstraint(PointConstraint):

    def __init__(self, h_sep=None, a_sep=None, p_sep=None, t_sep=None):
        from jasmin_cis.exceptions import InvalidCommandLineOptionError

        super(SepConstraint, self).__init__()

        self.checks = []

        if h_sep is not None:
            self.h_sep = jasmin_cis.utils.parse_distance_with_units_to_float_km(h_sep)
            self.checks.append(self.horizontal_constraint)
        if a_sep is not None:
            self.a_sep = jasmin_cis.utils.parse_distance_with_units_to_float_m(a_sep)
            self.checks.append(self.alt_constraint)
        if p_sep is not None:
            try:
                self.p_sep = float(p_sep)
            except:
                raise InvalidCommandLineOptionError('Separation Constraint p_sep must be a valid float')
            self.checks.append(self.pressure_constraint)
        if t_sep is not None:
            from jasmin_cis.time_util import parse_datetimestr_delta_to_float_days
            try:
                self.t_sep = parse_datetimestr_delta_to_float_days(t_sep)
            except ValueError as e:
                raise InvalidCommandLineOptionError(e)
            self.checks.append(self.time_constraint)

    def time_constraint(self, point, ref_point):
        return point.time_sep(ref_point) < self.t_sep

    def alt_constraint(self, point, ref_point):
        return point.alt_sep(ref_point) < self.a_sep

    def pressure_constraint(self, point, ref_point):
        return point.pres_sep(ref_point) < self.p_sep

    def horizontal_constraint(self, point, ref_point):
        return point.haversine_dist(ref_point) < self.h_sep

    def constrain_points(self, ref_point, data):
        con_points = HyperPointList()
        for point in data:
            if all(check(point, ref_point) for check in self.checks):
                con_points.append(point)
        return con_points


class SepConstraintKdtree(PointConstraint):
    """A separation constraint that uses a k-D tree to optimise spatial constraining.
    If no horizontal separation parameter is supplied, this reduces to an exhaustive
    search using the other parameter(s).
    """
    def __init__(self, h_sep=None, a_sep=None, p_sep=None, t_sep=None):
        from jasmin_cis.exceptions import InvalidCommandLineOptionError

        self.haversine_distance_kd_tree_index = False

        super(SepConstraintKdtree, self).__init__()

        self.checks = []
        if h_sep is not None:
            self.h_sep = jasmin_cis.utils.parse_distance_with_units_to_float_km(h_sep)
            self.haversine_distance_kd_tree_index = None

        if a_sep is not None:
            self.a_sep = jasmin_cis.utils.parse_distance_with_units_to_float_m(a_sep)
            self.checks.append(self.alt_constraint)
        if p_sep is not None:
            try:
                self.p_sep = float(p_sep)
            except:
                raise InvalidCommandLineOptionError('Separation Constraint p_sep must be a valid float')
            self.checks.append(self.pressure_constraint)
        if t_sep is not None:
            from jasmin_cis.time_util import parse_datetimestr_delta_to_float_days
            try:
                self.t_sep = parse_datetimestr_delta_to_float_days(t_sep)
            except ValueError as e:
                raise InvalidCommandLineOptionError(e)
            self.checks.append(self.time_constraint)

    def time_constraint(self, point, ref_point):
        return point.time_sep(ref_point) < self.t_sep

    def alt_constraint(self, point, ref_point):
        return point.alt_sep(ref_point) < self.a_sep

    def pressure_constraint(self, point, ref_point):
        return point.pres_sep(ref_point) < self.p_sep

    def horizontal_constraint(self, point, ref_point):
        return point.haversine_dist(ref_point) < self.h_sep

    def constrain_points(self, ref_point, data):
        con_points = HyperPointList()
        if self.haversine_distance_kd_tree_index:
            point_indices = self.haversine_distance_kd_tree_index.find_points_within_distance(ref_point, self.h_sep)
            for idx in point_indices:
                point = data[idx]
                if all(check(point, ref_point) for check in self.checks):
                    con_points.append(point)
        else:
            for point in data:
                if all(check(point, ref_point) for check in self.checks):
                    con_points.append(point)
        return con_points


class mean(Kernel):

    def get_value(self, point, data):
        '''
            Colocation using the mean of any points left after a constraint.
        '''
        from numpy import mean
        values = data.vals
        if len(values) == 0: raise ValueError
        return mean(values)


class stddev(Kernel):

    def get_value(self, point, data):
        """
        Colocation using the standard deviation of any points left after a constraint.
        """
        from numpy import std
        values = data.vals
        if len(values) < 2:
            raise ValueError
        return std(values, ddof=1)


class min(Kernel):

    def get_value(self, point, data):
        """
        Colocation using the standard deviation of any points left after a constraint.
        """
        values = data.vals
        if len(values) == 0:
            raise ValueError
        # Using builtin is required so that the class can be called min
        return __builtin__.min(values)


class max(Kernel):

    def get_value(self, point, data):
        """
        Colocation using the standard deviation of any points left after a constraint.
        """
        values = data.vals
        if len(values) == 0:
            raise ValueError
        # Using builtin is required so that the class can be called max
        return __builtin__.max(values)


class moments(Kernel):
    def __init__(self, mean_name='', stddev_name='', nopoints_name=''):
        self.mean_name = mean_name
        self.stddev_name = stddev_name
        self.nopoints_name = nopoints_name

    def get_variable_details(self, var_name, var_long_name, var_units):
        """Sets name and units for mean, standard deviation and number of points variables, based
        on those of the base variable or overridden by those specified as kernel parameters.
        :param var_name: base variable name
        :param var_long_name: base variable long name
        :param var_units: base variable units
        :return: tuple of tuples each containing (variable name, variable long name, variable units)
        """
        if self.mean_name == '':
            self.mean_name = var_name + '_mean'
        if self.stddev_name == '':
            self.stddev_name = var_name + '_std_dev'
        stdev_long_name = 'Standard deviation from the mean in ' + var_name
        stddev_units = var_units
        if self.nopoints_name == '':
            self.nopoints_name = var_name + '_no_points'
        npoints_long_name = 'Number of points used to calculate the mean of ' + var_name
        npoints_units = '1'
        return ((self.mean_name, var_long_name, var_units),
                (self.stddev_name, stdev_long_name, stddev_units),
                (self.nopoints_name, npoints_long_name, npoints_units))

    def get_value(self, point, data):
        """
        Returns the mean, standard deviation and number of values
        """
        from numpy import mean, std
        values = data.vals
        num_values = len(values)
        if num_values == 0:
            raise ValueError
        elif num_values == 1:
            std_dev = np.nan
        else:
            std_dev = std(values, ddof=1)
        return mean(values), std_dev, num_values


class nn_horizontal(Kernel):

    def get_value(self, point, data):
        '''
            Colocation using nearest neighbours along the face of the earth where both points and
              data are a list of HyperPoints. The default point is the first point.
        '''
        iterator = data.__iter__()
        try:
            nearest_point = iterator.next()
        except StopIteration:
            # No points to check
            raise ValueError
        for data_point in iterator:
            if point.compdist(nearest_point, data_point): nearest_point = data_point
        return nearest_point.val[0]


class nn_horizontal_kdtree(Kernel):
    def __init__(self):
        self.haversine_distance_kd_tree_index = None

    def get_value(self, point, data):
        """
        Colocation using nearest neighbours along the face of the earth using a k-D tree index.
        """
        nearest_index = self.haversine_distance_kd_tree_index.find_nearest_point(point)
        if nearest_index is None:
            raise ValueError
        if nearest_index > len(data):
            pass
        nearest_point = data[nearest_index]
        return nearest_point.val[0]


class nn_altitude(Kernel):

    def get_value(self, point, data):
        '''
            Colocation using nearest neighbours in altitude, where both points and
              data are a list of HyperPoints. The default point is the first point.
        '''
        iterator = data.__iter__()
        try:
            nearest_point = iterator.next()
        except StopIteration:
            # No points to check
            raise ValueError
        for data_point in iterator:
            if point.compalt(nearest_point, data_point): nearest_point = data_point
        return nearest_point.val[0]


class nn_pressure(Kernel):

    def get_value(self, point, data):
        '''
            Colocation using nearest neighbours in pressure, where both points and
              data are a list of HyperPoints. The default point is the first point.
        '''
        iterator = data.__iter__()
        try:
            nearest_point = iterator.next()
        except StopIteration:
            # No points to check
            raise ValueError
        for data_point in iterator:
            if point.comppres(nearest_point, data_point): nearest_point = data_point
        return nearest_point.val[0]


class nn_time(Kernel):

    def get_value(self, point, data):
        '''
            Colocation using nearest neighbours in time, where both points and
              data are a list of HyperPoints. The default point is the first point.
        '''
        iterator = data.__iter__()
        try:
            nearest_point = iterator.next()
        except StopIteration:
            # No points to check
            raise ValueError
        for data_point in iterator:
            if point.comptime(nearest_point, data_point): nearest_point = data_point
        return nearest_point.val[0]


# These classes act as abbreviations for kernel classes above:
class nn_h(nn_horizontal):
    """Nearest neighbour horizontal kernel - alias for nn_horizontal.
    """
    pass


class nn_a(nn_altitude):
    """Nearest neighbour altitude kernel - alias for nn_altitude.
    """
    pass


class nn_p(nn_pressure):
    """Nearest neighbour pressure kernel - alias for nn_pressure.
    """
    pass


class nn_t(nn_time):
    """Nearest neighbour time kernel - alias for nn_time.
    """
    pass


class nn_gridded(Kernel):
    def get_value(self, point, data):
        """
        Co-location routine using nearest neighbour algorithm optimized for gridded data.
        This calls out to iris to do the work.
        """
        from iris.analysis.interpolate import nearest_neighbour_data_value

        # Remove any tuples in the list that do not correspond to a dimension coordinate in the cube 'data'.
        new_coord_tuple_list = []
        for i in point.coord_tuple:
            if len(data.coords(i[0], dim_coords=True)) > 0:
                new_coord_tuple_list.append(i)
        point.coord_tuple = new_coord_tuple_list

        return nearest_neighbour_data_value(data, point.coord_tuple)


class li(Kernel):
    def get_value(self, point, data):
        """
        Co-location routine using iris' linear interpolation algorithm. This only makes sense for gridded data.
        """
        from iris.analysis.interpolate import linear

        # Remove any tuples in the list that do not correspond to a dimension coordinate in the cube 'data'.
        new_coord_tuple_list = []
        for i in point.coord_tuple:
            if len(data.coords(i[0], dim_coords=True)) > 0:
                new_coord_tuple_list.append(i)
        point.coord_tuple = new_coord_tuple_list

        return linear(data, point.coord_tuple).data


class GriddedColocatorUsingIrisRegrid(Colocator):

    def __init__(self, var_name='', var_long_name='', var_units='', missing_data_for_missing_sample=False):
        super(Colocator, self).__init__()
        self.var_name = var_name
        self.var_long_name = var_long_name
        self.var_units = var_units
        self.missing_data_for_missing_sample = missing_data_for_missing_sample

    def check_for_valid_kernel(self, kernel):
        from jasmin_cis.exceptions import ClassNotFoundError

        if not (isinstance(kernel, gridded_gridded_nn) or isinstance(kernel, gridded_gridded_li)):
            raise ClassNotFoundError("Expected kernel of one of classes {}; found one of class {}".format(
                str([jasmin_cis.utils.get_class_name(gridded_gridded_nn),
                    jasmin_cis.utils.get_class_name(gridded_gridded_li)]),
                    jasmin_cis.utils.get_class_name(type(kernel))))

    def colocate(self, points, data, constraint, kernel):
        """
        This colocator takes two Iris cubes, and colocates from the data cube onto the grid of the points cube. The
        colocator then returns another Iris cube. This uses Iris' implementation, which only works onto a horizontal
        grid.
        :param points: An Iris cube with the sampling grid to colocate onto.
        :param data: The Iris cube with the data to be colocated.
        :param constraint: None allowed yet, as this is unlikely to be required for gridded-gridded.
        :param kernel: The kernel to use, current options are gridded_gridded_nn and gridded_gridded_li.
        :return: An Iris cube with the colocated data.
        """
        import iris
        self.check_for_valid_kernel(kernel)
        new_data = iris.analysis.interpolate.regrid(data, points, mode=kernel.name)#, **kwargs)

        return [new_data]


class GriddedColocator(GriddedColocatorUsingIrisRegrid):

    def colocate(self, points, data, constraint, kernel):
        """
        This colocator takes two Iris cubes, and colocates from the data cube onto the grid of the 'points' cube. The
        colocator then returns another Iris cube.
        :param points: An Iris cube with the sampling grid to colocate onto.
        :param data: The Iris cube with the data to be colocated.
        :param constraint: None allowed yet, as this is unlikely to be required for gridded-gridded.
        :param kernel: The kernel to use, current options are gridded_gridded_nn and gridded_gridded_li.
        :return: An Iris cube with the colocated data.
        """

        self.check_for_valid_kernel(kernel)

        # Force the data longitude range to be the same as that of the sample grid.
        _fix_cube_longitude_range(points.coords(), data)

        # Initialise variables used to create an output mask based on the sample data mask.
        sample_coord_lookup = {}
        for idx, coord in enumerate(points.dim_coords):
            sample_coord_lookup[coord] = idx
        sample_coord_transpose_map = []
        other_coord_transpose_map = []
        repeat_size = 1
        output_mask = np.ma.nomask

        # Make a list of the coordinates we have, with each entry containing a list with the name of the coordinate and
        # the number of points along its axis. One is for the sample grid, which contains the points where we
        # interpolate too, and one is for the output grid, which will additionally contain any dimensions missing in the
        # sample grid.
        coord_names_and_sizes_for_sample_grid = []
        coord_names_and_sizes_for_output_grid = []
        for idx, coord in enumerate(data.coords(dim_coords=True)):
            # First try and find the coordinate in points, the sample grid. If an exception is thrown, it means that
            # name does not appear in the sample grid, and instead take the coordinate name and length from the original
            # data, as this is what we will be keeping.
            try:
                sample_coord = points.coords(coord.name(), dim_coords=True)[0]
                coord_names_and_sizes_for_sample_grid.append([coord.name(), len(sample_coord.points)])
                # Find the index of the sample coordinate corresponding to the data coordinate.
                sample_coord_transpose_map.append(sample_coord_lookup[sample_coord])
            except IndexError:
                coord_names_and_sizes_for_output_grid.append([coord.name(), len(coord.points)])
                repeat_size *= len(coord.points)
                other_coord_transpose_map.append(idx)

        # Adding the lists together in this way ensures that the coordinates not in the sample grid appear in the final
        # position, which is important for adding the points from the Iris interpolater to the new array. The data
        # returned from the Iris interpolater method will have dimensions of these missing coordinates, which needs
        # to be the final dimensions in the numpy array, as the iterator will give the position of the other dimensions.
        coord_names_and_sizes_for_output_grid = coord_names_and_sizes_for_sample_grid + \
                                                coord_names_and_sizes_for_output_grid

        # An array for the colocated data, with the correct shape
        output_shape = tuple(i[1] for i in coord_names_and_sizes_for_output_grid)
        new_data = np.zeros(output_shape)

        if self.missing_data_for_missing_sample:
            output_mask = self._make_output_mask(coord_names_and_sizes_for_sample_grid, kernel,
                                                 other_coord_transpose_map, output_shape, points,
                                                 repeat_size, sample_coord_transpose_map)

        # Now recreate the points cube, while ignoring any DimCoords in points that are not in the data cube
        new_dim_coord_list = []
        new_points_array_shape = []
        for i in range(0, len(coord_names_and_sizes_for_output_grid)):
            # Try and find the coordinate in the sample grid
            coord_found = points.coords(coord_names_and_sizes_for_output_grid[i][0])

            # If the coordinate exists in the sample grid then append the new coordinate to the list. Iris requires
            # this be given as a DimCoord object, along with a axis number, in a tuple pair.
            if len(coord_found) != 0:
                new_dim_coord_list.append((coord_found[0], len(new_dim_coord_list)))
                new_points_array_shape.append(coord_found[0].points.size)

        new_points_array = np.zeros(tuple(new_points_array_shape))

        # Use the new_data array to recreate points, without the DimCoords not in the data cube
        points = iris.cube.Cube(new_points_array, dim_coords_and_dims=new_dim_coord_list)

        # Iris has a different interface for iris.analysis.interpolate.extract_nearest_neighbour, compared to
        # iris.analysis.interpolate.linear, so we need need to make an exception for how we treat the linear
        # interpolation case.
        if kernel.name == 'bilinear':
            output_cube = self._colocate_bilinear(coord_names_and_sizes_for_sample_grid, data, kernel, output_mask,
                                                  points)
        else:
            output_cube = self._colocate_nearest(coord_names_and_sizes_for_output_grid,
                                                 coord_names_and_sizes_for_sample_grid, data, kernel, new_data,
                                                 output_mask, points)
        return [output_cube]

    @staticmethod
    def _make_output_mask(coord_names_and_sizes_for_sample_grid, kernel, other_coord_transpose_map,
                          output_shape, points, repeat_size, sample_coord_transpose_map):
        """ Creates a mask to apply to the output data based on the sample data mask, but rearranged to match
        the coordinate order of the output cube. This order depends on the kernel. If there are coordinates in
        the data grid that are not in the sample grid, the same mask value is repeated for all values of the
        extra coordinates. If there are coordinates in the sample grid that are not in the data grid, a mask
        is not created since there is many to one correspondence between sample and output grid points.
        """
        output_mask = None

        # Construct the missing value mask from the sample data, if applicable.
        if len(coord_names_and_sizes_for_sample_grid) < len(points.dim_coords):
            # One or more axes collapsed so many sample points correspond to each output point.
            pass
        else:
            input_mask = np.ma.getmask(points.data)
            if input_mask is np.ma.nomask:
                # No sample data missing-value mask.
                pass
            else:
                # Transpose the mask from the sample cube to match the coordinate order of the
                # the data coordinates (but only including those in common with the sample cube).
                output_mask = np.transpose(points.data.mask, sample_coord_transpose_map)

                # Fill in the remaining coordinates by repeating the constructed mask for each value
                # of those coordinates. This matches the coordinate order for the nearest neighbour kernel.
                output_mask = np.reshape(np.repeat(output_mask, repeat_size), output_shape)

                if kernel.name == 'bilinear':
                    # iris.analysis.interpolate.linear returns the colocated data in a cube with
                    # the coordinates in the order of the input data. Transpose the mask back to
                    # the data coordinate order.
                    inv_transpose_map = []
                    for i in xrange(len(output_shape)):
                        if i not in other_coord_transpose_map:
                            inv_transpose_map.append(i)
                    inv_transpose_map.extend(other_coord_transpose_map)
                    transpose_map = [None] * len(inv_transpose_map)
                    for i in range(len(inv_transpose_map)):
                        transpose_map[inv_transpose_map[i]] = i
                    output_mask = np.transpose(output_mask, transpose_map)

        return output_mask

    @staticmethod
    def _colocate_bilinear(coord_names_and_sizes_for_sample_grid, data, kernel, output_mask, points):
        """ Colocates using iris.analysis.interpolate.linear
        """
        coordinate_point_pairs = []
        for j in range(0, len(coord_names_and_sizes_for_sample_grid)):
            # For each coordinate make the list of tuple pair Iris requires, for example
            # [('latitude', -90), ('longitude, 0')]
            coordinate_point_pairs.append((coord_names_and_sizes_for_sample_grid[j][0],
                                           points.dim_coords[j].points))

        # The result here will be a cube with the correct dimensions for the output, so interpolated over all points
        # in coord_names_and_sizes_for_output_grid.
        output_cube = make_from_cube(kernel.interpolater(data, coordinate_point_pairs))
        output_cube.data = jasmin_cis.utils.apply_mask_to_numpy_array(output_cube.data, output_mask)
        return output_cube

    @staticmethod
    def _colocate_nearest(coord_names_and_sizes_for_output_grid, coord_names_and_sizes_for_sample_grid,
                          data, kernel, new_data, output_mask, points):
        """ Colocate using iris.analysis.interpolate.extract_nearest_neighbour.
        """
        # index_iterator returns an iterator over every dimension stored in coord_names_and_sizes_for_sample_grid.
        # Now for each point in the sample grid we do the interpolation.
        for i in jasmin_cis.utils.index_iterator([i[1] for i in coord_names_and_sizes_for_sample_grid]):
            coordinate_point_pairs = []
            for j in range(0, len(coord_names_and_sizes_for_sample_grid)):
                # For each coordinate make the list of tuple pair Iris requires, for example
                # [('latitude', -90), ('longitude, 0')]
                coordinate_point_pairs.append((coord_names_and_sizes_for_sample_grid[j][0],
                                               points.dim_coords[j].points[i[j]]))

            # The result here will either be a single data value, if the sample grid and data have matching
            # coordinates, or an array if the data grid as more coordinate dimensions than the sample grid. The Iris
            # interpolation functions actually return a Cube.
            new_data[i] = kernel.interpolater(data, coordinate_point_pairs).data

            # Log a progress update, as this can take a long time.
            if all(x == 0 for x in i[1:]):
                logging.info('Currently on {0} coordinate at {1}'.format(
                    coord_names_and_sizes_for_sample_grid[0][0], points.dim_coords[0].points[i[0]]))

        # Now we need to make a list with the appropriate coordinates, i.e. based on that in
        # coord_names_and_sizes_for_output_grid. This means choosing the grid points from the sampling grid in the
        # case of coordinates that exist in both the data and the sample grid, and taking the points from the
        # sampling grid otherwise.
        new_dim_coord_list = []
        for i in range(0, len(coord_names_and_sizes_for_output_grid)):
            # Try and find the coordinate in the sample grid
            coord_found = points.coords(coord_names_and_sizes_for_output_grid[i][0])

            # If the coordinate did not exist in the sample grid then look for it in the data grid
            if len(coord_found) == 0:
                coord_found = data.coords(coord_names_and_sizes_for_output_grid[i][0])

            # Append the new coordinate to the list. Iris requires this be given as a DimCoord object, along with a
            # axis number, in a tuple pair.
            new_dim_coord_list.append((iris.coords.DimCoord(coord_found[0].points,
                                                            standard_name=coord_found[0].standard_name,
                                                            long_name=coord_found[0].long_name,
                                                            units=coord_found[0].units), i))

        # Finally return the new cube with the colocated data. jasmin_cis.col requires this be returned as a list of
        # Cube objects.
        output_cube = GriddedData(new_data, dim_coords_and_dims=new_dim_coord_list, var_name=data.var_name,
                                  long_name=data.long_name, units=data.units, attributes=data.attributes)
        output_cube.data = jasmin_cis.utils.apply_mask_to_numpy_array(output_cube.data, output_mask)
        return output_cube


class gridded_gridded_nn(Kernel):
    def __init__(self):
        self.name = 'nearest'
        self.interpolater = iris.analysis.interpolate.extract_nearest_neighbour

    def get_value(self, point, data):
        '''Not needed for gridded/gridded co-location.
        '''
        raise ValueError("gridded_gridded_nn kernel selected for use with colocator other than GriddedColocator")


class gridded_gridded_li(Kernel):
    def __init__(self):
        self.name = 'bilinear'
        self.interpolater = iris.analysis.interpolate.linear

    def get_value(self, point, data):
        '''Not needed for gridded/gridded co-location.
        '''
        raise ValueError("gridded_gridded_li kernel selected for use with colocator other than GriddedColocator")


class GeneralGriddedColocator(Colocator):
    """Performs co-location of data on to the points of a cube.
    """

    def __init__(self, fill_value=None, var_name='', var_long_name='', var_units='',
                 missing_data_for_missing_sample=False):
        super(GeneralGriddedColocator, self).__init__()
        if fill_value is not None:
            try:
                self.fill_value = float(fill_value)
            except ValueError:
                raise jasmin_cis.exceptions.InvalidCommandLineOptionError(
                    'Dummy Constraint fill_value must be a valid float')
        self.var_name = var_name
        self.var_long_name = var_long_name
        self.var_units = var_units
        self.missing_data_for_missing_sample = missing_data_for_missing_sample

    def colocate(self, points, data, constraint, kernel):
        """
        :param points: cube defining the sample points
        :param data: CommonData object providing data to be co-located
        :param constraint: instance of a Constraint subclass, which takes a data object and returns a subset of that
                           data based on it's internal parameters
        :param kernel: instance of a Kernel subclass which takes a number of points and returns a single value
        :return: Cube of co-located data
        """
        data_points = data.get_non_masked_points()

        # Work out how to iterate over the cube and map HyperPoint coordinates to cube coordinates.
        coord_map = make_coord_map(points, data)
        coords = points.coords()
        shape = []
        output_coords = []

        # Find shape of coordinates to be iterated over.
        for (hpi, ci, shi) in coord_map:
            coord = coords[ci]
            if coord.ndim > 1:
                raise NotImplementedError("Co-location of data onto a cube with a coordinate of dimension greater"
                                          " than one is not supported (coordinate %s)", coord.name())
            # Ensure that bounds exist.
            if not coord.has_bounds():
                logging.warning("Creating guessed bounds as none exist in file")
                coord.guess_bounds()
            shape.append(coord.shape[0])
            output_coords.append(coord)

        _fix_longitude_range(coords, data_points)

        # Create index if constraint supports it.
        data_index.create_indexes(constraint, coords, data_points, coord_map)
        data_index.create_indexes(kernel, points, data_points, coord_map)

        # Initialise output array as initially all masked, and set the appropriate fill value.
        values = np.ma.zeros(shape)
        values.mask = True
        values.fill_value = self.fill_value

        logging.info("--> Co-locating...")

        # Iterate over cells in cube.
        num_cells = np.product(shape)
        cell_count = 0
        cell_total = 0
        is_indexed_constraint = isinstance(constraint, IndexedConstraint)
        is_cell_constraint = isinstance(constraint, CellConstraint)
        for indices in jasmin_cis.utils.index_iterator(shape):
            if not self.missing_data_for_missing_sample or points.data[indices] is not np.ma.masked:
                hp_values = [None] * HyperPoint.number_standard_names
                hp_cell_values = [None] * HyperPoint.number_standard_names
                for (hpi, ci, shi) in coord_map:
                    hp_values[hpi] = coords[ci].points[indices[shi]]
                    hp_cell_values[hpi] = coords[ci].cell(indices[shi])

                hp = HyperPoint(*hp_values)
                if is_indexed_constraint:
                    arg = indices
                elif is_cell_constraint:
                    arg = HyperPoint(*hp_cell_values)
                else:
                    arg = hp
                con_points = constraint.constrain_points(arg, data_points)
                try:
                    values[indices] = kernel.get_value(hp, con_points)
                except ValueError:
                    pass

            # Log progress periodically.
            cell_count += 1
            cell_total += 1
            if cell_count == 10000:
                logging.info("    Processed %d points of %d (%d%%)", cell_total, num_cells, int(cell_total * 100 / num_cells))
                cell_count = 0

        # Construct an output cube containing the colocated data.
        cube = self._create_colocated_cube(points, data, values, output_coords, self.fill_value)
        data_with_nan_and_inf_removed = np.ma.masked_invalid(cube.data)
        data_with_nan_and_inf_removed.set_fill_value(self.fill_value)
        cube.data = data_with_nan_and_inf_removed

        return [cube]

    def _create_colocated_cube(self, src_cube, src_data, data, coords, fill_value):
        """Creates a cube using the metadata from the source cube and supplied data.

        :param src_cube: cube of sample points
        :param src_data: ungridded data that was to be colocated
        :param data: colocated data values
        :param coords: coordinates for output cube
        :param fill_value: value that has been used as the fill value in data
        :return: cube of colocated data
        """
        dim_coords_and_dims = []
        for idx, coord in enumerate(coords):
            dim_coords_and_dims.append((coord, idx))
        metadata = src_data.metadata
        metadata.missing_value = fill_value
        cube = GriddedData(data, standard_name=src_data.standard_name,
                           long_name=src_data.long_name,
                           var_name=src_data.var_name,
                           units=src_data.units,
                           dim_coords_and_dims=dim_coords_and_dims)
        #TODO Check if any other keyword arguments should be set:
        # cube = iris.cube.Cube(data, standard_name=None, long_name=None, var_name=None, units=None,
        #                       attributes=None, cell_methods=None, dim_coords_and_dims=None, aux_coords_and_dims=None,
        #                       aux_factories=None, data_manager=None)
        return cube


class CubeCellConstraint(CellConstraint):
    """Constraint for constraining HyperPoints to be within an iris.coords.Cell.
    """
    def constrain_points(self, sample_point, data):
        """Returns HyperPoints lying within a cell.
        :param sample_point: HyperPoint of cells defining sample region
        :param data: list of HyperPoints to check
        :return: HyperPointList of points found within cell
        """
        con_points = HyperPointList()
        for point in data:
            include = True
            for idx in xrange(HyperPoint.number_standard_names):
                cell = sample_point[idx]
                if cell is not None:
                    if not (np.min(cell.bound) <= point[idx] < np.max(cell.bound)):
                        include = False
            if include:
                con_points.append(point)
        return con_points


class BinningCubeCellConstraint(IndexedConstraint):
    """Constraint for constraining HyperPoints to be within an iris.coords.Cell.

    Uses the index_data method to bin all the points
    """
    def __init__(self):
        super(BinningCubeCellConstraint, self).__init__()
        self.grid_cell_bin_index = None

    def constrain_points(self, sample_point, data):
        """Returns HyperPoints lying within a cell.

        This implementation returns the points that have been stored in the
        appropriate bin by the index_data method.
        :param sample_point: HyperPoint of indices of cells defining sample region
        :param data: list of HyperPoints to check
        :return: HyperPointList of points found within cell
        """
        point_list = self.grid_cell_bin_index.get_points_by_indices(sample_point)
        con_points = HyperPointList()
        if point_list is not None:
            for point in point_list:
                con_points.append(data[point])
        return con_points


def make_coord_map(points, data):
    # If there are coordinates in the sample grid that are not present for the data,
    # omit the from the set of coordinates in the output grid. Find a mask of coordinates
    # that are present to use when determining the output grid shape.
    coordinate_mask = [False if c is None else True for c in data.find_standard_coords()]

    # Find the mapping of standard coordinates to those in the sample points and those to be used
    # in the output data.
    return _find_standard_coords(points, coordinate_mask)


def _find_standard_coords(cube, coordinate_mask):
    """Finds the mapping of sample point coordinates to the standard ones used by HyperPoint.

    :param cube: cube among the coordinates of which to find the standard coordinates
    :param coordinate_mask: list of booleans indicating HyperPoint coordinates that are present
    :return: list of tuples relating index in HyperPoint to index in coords and in coords to be iterated over
    """
    coord_map = []
    coord_lookup = {}
    # for idx, coord in enumerate(cube.coords()):
    coords = cube.coords()
    for idx, coord in enumerate(coords):
        coord_lookup[coord] = idx

    shape_idx = 0
    for hpi, name in enumerate(HyperPoint.standard_names):
        if coordinate_mask[hpi]:
            # Get the dimension coordinates only - these correspond to dimensions of data array.
            coords = cube.coords(standard_name=name, dim_coords=True)
            if len(coords) > 1:
                msg = ('Expected to find exactly 1 coordinate, but found %d. They were: %s.'
                       % (len(coords), ', '.join(coord.name() for coord in coords)))
                raise jasmin_cis.exceptions.CoordinateNotFoundError(msg)
            elif len(coords) == 1:
                coord_map.append((hpi, coord_lookup[coords[0]], shape_idx))
                shape_idx += 1
    return coord_map


def _find_longitude_range(coords):
    """Finds the start of the longitude range, assumed to be either 0,360 or -180,180
    :param coords: coordinates to check
    :return: starting value for longitude range or None if no longitude coordinate found
    """
    low = None
    for coord in coords:
        if coord.standard_name == 'longitude':
            low = 0.0
            min_val = coord.points.min()
            if min_val < 0.0:
                low = -180.0
    return low


def _fix_longitude_range(coords, data_points):
    """Sets the longitude range of the data points to match that of the sample coordinates.
    :param coords: coordinates for grid on which to colocate
    :param data_points: HyperPointList of data to fix
    """
    range_start = _find_longitude_range(coords)
    if range_start is not None:
        data_points.set_longitude_range(range_start)


def _fix_cube_longitude_range(coords, data):
    """Sets the longitude range of the data cube to match that of the sample coordinates.
    :param coords: coordinates for grid on which to colocate
    :param data: cube of data to fix
    """
    range_start = _find_longitude_range(coords)
    if range_start is not None:
        data.set_longitude_range(range_start)
