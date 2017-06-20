import numpy.testing as npt

from utilities import learning_data


class Test:

    def test_get_variable_type_indices(self):
        npt.assert_array_equal(learning_data.get_variable_type_indices([[]]), [])
        days = []
        days.append([1, 3, 5])
        npt.assert_array_equal(learning_data.get_variable_type_indices(days), [2])
        days.append([])
        npt.assert_array_equal(learning_data.get_variable_type_indices(days), [2])
        days.append([6, 7, 8])
        npt.assert_array_equal(learning_data.get_variable_type_indices(days), [2, 5])

    def test_get_hdf_variable_names(self):
        npt.assert_array_equal(learning_data.get_hdf_variable_names([], []), [])
        days = []
        days.append([1, 3, 5])
        name_prefixes = ['cat']
        npt.assert_array_equal(learning_data.get_hdf_variable_names(days, name_prefixes),
                               ['cat_1', 'cat_3', 'cat_5'])
        days.append([6, 7, 8])
        name_prefixes.append('dog')
        npt.assert_array_equal(learning_data.get_hdf_variable_names(days, name_prefixes),
                               ['cat_1', 'cat_3', 'cat_5', 'dog_6', 'dog_7', 'dog_8'])

