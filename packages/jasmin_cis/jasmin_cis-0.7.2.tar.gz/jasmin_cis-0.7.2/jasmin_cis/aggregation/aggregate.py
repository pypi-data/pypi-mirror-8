import logging
import iris.analysis
import iris.coords
import iris.coord_categorisation
from jasmin_cis.aggregation.aggregator import Aggregator
from jasmin_cis.col_framework import get_kernel
from jasmin_cis.data_io.read import read_data
from jasmin_cis.exceptions import CISError, InvalidVariableError
from jasmin_cis.cis import __version__
from jasmin_cis.aggregation.aggregation_kernels import aggregation_kernels
from iris.exceptions import IrisError
from jasmin_cis.utils import remove_file_prefix


class Aggregate():
    def __init__(self, grid, output_file):
        self.grid = grid
        self._output_file = output_file

    def aggregate(self, variable, filenames, product, kernel_name):

        # Read the input data - the parser limits the number of data groups to one for this command.
        try:
            # Read the data into a data object (either UngriddedData or Iris Cube), concatenating data from
            # the specified files.
            logging.info("Reading data for variable: %s", variable)
            data = read_data(filenames, variable, product)
        except (IrisError, InvalidVariableError) as e:
            raise CISError("There was an error reading in data: \n" + str(e))
        except IOError as e:
            raise CISError("There was an error reading one of the files: \n" + str(e))

        aggregator = Aggregator(data, self.grid)

        if isinstance(data, iris.cube.Cube):
            kernel = aggregation_kernels[kernel_name]
            data = aggregator.aggregate_gridded(kernel)
        else:
            kernel_class = get_kernel(kernel_name)
            kernel = kernel_class()
            data = aggregator.aggregate_ungridded(kernel)

        #TODO Tidy up output of grid in the history
        history = "Subsetted using CIS version " + __version__ + \
                  "\n variable: " + str(variable) + \
                  "\n from files: " + str(filenames) + \
                  "\n using new grid: " + str(self.grid) + \
                  "\n with kernel: " + kernel_name + "."
        data.add_history(history)

        data.save_data(self._output_file)

