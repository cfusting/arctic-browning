import numpy

from experiments import lesser_scaup

NAME = 'TuftedDuck'


class TuftedDuck(lesser_scaup.LesserScaup):

    def __init__(self):
        super(TuftedDuck, self).__init__()

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(TuftedDuck, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)

        def safe_sqrt(x):
            x = numpy.sqrt(x)
            if isinstance(x, numpy.ndarray):
                x[numpy.isnan(x)] = 0
            elif numpy.isnan(x):
                x = 0
            return x
        pset.addPrimitive(safe_sqrt, 1)
        pset.addPrimitive(numpy.cbrt, 1)
        return pset
