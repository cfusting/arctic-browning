import math
from functools import partial

from gp.parametrized import simple_parametrized_terminals as sp
from gp.algorithms import afpo, operators
from gp.parametrized import mutation

from experiments import control

NAME = 'Mandarin'


class Mandarin(control.Control):

    def __init__(self):
        super(Mandarin, self).__init__()

    def get_toolbox(self, predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                    test_response=None):
        toolbox = super(Mandarin, self).get_toolbox(predictors, response, pset, variable_type_indices, variable_names,
                                                    test_predictors=None, test_response=None)
        mutations = [partial(sp.mutate_parametrized_nodes, stdev_calc=math.sqrt),
                     partial(operators.mutation_biased, expr=toolbox.grow, node_selector=toolbox.koza_node_selector)]
        toolbox.register("mutate", mutation.multi_mutation_exclusive, mutations=mutations, probs=[.5, .5])
        toolbox.register("run", afpo.pareto_optimization, population=self.pop, toolbox=toolbox,
                         xover_prob=self.XOVER_PROB, mut_prob=self.MUT_PROB, ngen=self.NGEN,
                         tournament_size=self.TOURNAMENT_SIZE,  num_randoms=self.NUM_RANDOMS, stats=self.mstats,
                         archive=self.multi_archive, calc_pareto_front=False, verbose=False, reevaluate_population=True)
        return toolbox

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(Mandarin, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)
        pset.add_parametrized_terminal(sp.RangeOperationTerminal)
        return pset
