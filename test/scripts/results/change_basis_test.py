import numpy
import numpy.testing as npt

import utilities.design_matrix
import utilities.learning_data
from utilities import learning_data, feature
from scripts.results import change_basis as cb
from experiments import control as experiment


class ChangeBasisTests:

    def __init__(self):
        self.pset = None
        self.validation_toolbox = None

    def initialize(self, training_data):
        pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                                   training_data.variable_names, training_data.variable_dict)
        pset.addPrimitive(numpy.power, 2)
        self.pset = pset
        self.validation_toolbox = experiment.get_validation_toolbox(training_data.predictors, training_data.response,
                                                                    pset)

    def test_build_basis_and_feature_names(self):
        training_data = build_random_training_data((10, 10))
        self.initialize(training_data)
        features = []
        i = 0
        while i < 3:
            features.append(feature.Feature(None, None))


def build_random_training_data(shape):
    training_data = learning_data.LearningData()
    training_data.num_observations = shape[0]
    training_data.num_variables = shape[1]
    training_data.predictors = numpy.random.rand(training_data.num_observations, training_data.num_variables)
    training_data.response = numpy.random.rand(training_data.num_observations, 1)
    training_data.variable_names = utilities.design_matrix.get_simple_variable_names(training_data.num_variables)
    training_data.variable_type_indices = \
        learning_data.get_default_variable_type_indices(training_data.num_variables)
    training_data.variable_dict = utilities.learning_data.get_simple_variable_dict(training_data.num_variables)
    return training_data


