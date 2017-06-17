from gp.parametrized import simple_parametrized_terminals as sp

from experiments import mandarin

NAME = "WhistlingDuck"


class WhistlingDuck(mandarin.Mandarin):

    def __init__(self):
        super(WhistlingDuck, self).__init__()

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(WhistlingDuck, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)
        pset.add_parametrized_terminal(sp.MomentFindingTerminal)
        return pset
