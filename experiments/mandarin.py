from gp.parametrized import simple_parametrized_terminals as sp

from experiments import control_mandarin

NAME = "Mandarin"


class Mandarin(control_mandarin.ControlMandarin):

    def __init__(self):
        super(Mandarin, self).__init__()

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(Mandarin, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)
        pset.add_parametrized_terminal(sp.RangeOperationTerminal)
        return pset
