import numpy.testing as npt
import numpy as np
from pyhdf.SD import SD, SDC

from utilities import learning_data as ld


class Test:

    def test_get_unique_variable_prefixes(self):
        variable_names = ['penguin0', 'penguin1']
        npt.assert_array_equal(ld.get_unique_variable_prefixes(variable_names), ['penguin'])
        variable_names.append('ferret0')
        npt.assert_array_equal(ld.get_unique_variable_prefixes(variable_names), ['penguin', 'ferret'])

    def test_get_variable_groups(self):
        variable_names = ['penguin0', 'penguin1']
        unique_prefixes = ld.get_unique_variable_prefixes(variable_names)
        npt.assert_array_equal(ld.get_variable_groups(variable_names, unique_prefixes),
                               [['penguin0', 'penguin1']])
        variable_names.append('ferret0')
        unique_prefixes = ld.get_unique_variable_prefixes(variable_names)
        npt.assert_array_equal(ld.get_variable_groups(variable_names, unique_prefixes),
                               [['penguin0', 'penguin1'], ['ferret0']])

    def test_get_variable_type_indices(self):
        npt.assert_array_equal(ld.get_variable_type_indices([[]]), [])
        variable_groups = [['penguin0', 'penguin1']]
        npt.assert_array_equal(ld.get_variable_type_indices(variable_groups), [1])
        variable_groups.append([])
        npt.assert_array_equal(ld.get_variable_type_indices(variable_groups), [1])
        variable_groups.append(['ferret0'])
        npt.assert_array_equal(ld.get_variable_type_indices(variable_groups), [1, 2])

    def test_to_from_hdf(self, tmpdir):
        file_name = str(tmpdir) + "/penguin.hdf"
        variable_names = ['lst1', 'lst2', 'lst3', 'snow1', 'snow2', 'ndvi1', 'ndvi2', 'ndvi3', 'ndvi4', 'ndvi5']
        dat = np.random.rand(10, 11)
        years = range(10)
        learning_data = ld.LearningData()
        learning_data.from_data(dat, variable_names, 'penguin')
        learning_data.meta_layers['years'] = np.array(years)
        learning_data.attributes = {'penguin': 'yes', 'tophat': 'no'}
        learning_data.to_hdf(file_name)
        training_data = ld.LearningData()
        training_data.from_hdf(file_name)
        assert training_data.num_variables == 10
        assert training_data.num_observations == 10
        npt.assert_array_equal(training_data.variable_names, ['lst1', 'lst2', 'lst3', 'snow1', 'snow2', 'ndvi1',
                               'ndvi2', 'ndvi3', 'ndvi4', 'ndvi5'])
        npt.assert_array_equal(training_data.unique_variable_prefixes, ['lst', 'snow', 'ndvi'])
        npt.assert_array_equal(training_data.variable_type_indices, [2, 4, 9])
        assert training_data.name == 'penguin'
        npt.assert_array_equal(training_data.meta_layers['years'], np.array(years))
        npt.assert_array_equal(training_data.predictors, dat[:, :-1])
        npt.assert_array_equal(training_data.response, dat[:, -1])
        npt.assert_array_equal(training_data.design_matrix.dat, dat)
        assert training_data.attributes['penguin'] == 'yes'
        assert training_data.attributes['tophat'] == 'no'

    def test_good_values(self):
        dat = np.random.rand(10, 11)
        dat[1, 2] = np.inf
        dat[5, 3] = -np.inf
        dat[7, 9] = np.nan
        dat[9, 3] = np.inf
        learning_data = ld.LearningData()
        learning_data.from_data(dat, None, 'penguin')
        assert np.isnan(learning_data.predictors).any() == False
        assert np.isfinite(learning_data.predictors).all() == True
