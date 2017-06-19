from abc import ABCMeta, abstractmethod


class Experiment:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_toolbox(self, predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                    test_response=None):
        pass

    @abstractmethod
    def get_validation_toolbox(self, predictors, response, pset, size_measure=None, fitness_class=None,
                               expression_dict=None):
        pass

    @abstractmethod
    def transform_features(self, predictors, response, predictor_transformer=None, response_transformer=None):
        pass

    @abstractmethod
    def get_pset(self, num_predictors, variable_type_indices, variable_names, variable_dict):
        pass



