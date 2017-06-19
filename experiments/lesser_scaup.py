from gp.parametrized import simple_parametrized_terminals as sp

from experiments import mandarin

NAME = 'LesserScaup'


class LesserScaup(mandarin.Mandarin):

    def __init__(self):
        super(LesserScaup, self).__init__()

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(LesserScaup, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)
        for i in range(1, 9):
            pset.add_parametrized_terminal(sp.RangeOperationTerminal)
        for i in range(1, 10):
            pset.add_parametrized_terminal(sp.MomentFindingTerminal)
        return pset
