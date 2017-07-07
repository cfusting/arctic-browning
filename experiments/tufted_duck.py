import numpy

from experiments import lesser_scaup

NAME = 'TuftedDuck'


class TuftedDuck(lesser_scaup.LesserScaup):

    def __init__(self):
        super(TuftedDuck, self).__init__()

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(TuftedDuck, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)

        def safe_sqrt(x):
            result = numpy.sqrt(x)
            if result == numpy.nan:
                result = 0
            return result
        pset.addPrimitive(safe_sqrt, 1)
        pset.addPrimitive(numpy.cbrt, 1)
        return pset
