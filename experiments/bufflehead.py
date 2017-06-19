import cachetools
import numpy
from functools import partial

from gp.algorithms import afpo, operators, subset_selection
from gp.parametrized import simple_parametrized_terminals as sp
from gp.parametrized import mutation

from experiments import mandarin

NAME = 'Bufflehead'


class Bufflehead(mandarin.Mandarin):

    def __init__(self):
        super(Bufflehead, self).__init__()

    def get_toolbox(self, predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                    test_response=None):

        toolbox = super(Bufflehead, self).get_toolbox(predictors, response, pset, variable_type_indices, variable_names,
                                                      test_predictors=None, test_response=None)
        expression_dict = cachetools.LRUCache(maxsize=1000)
        tiny_subset_selection_archive = subset_selection.RandomSubsetSelectionArchive(
            frequency=self.SUBSET_CHANGE_FREQUENCY,
            predictors=predictors,
            response=response,
            subset_size=int(self.SUBSET_SIZE * .1),
            expression_dict=expression_dict)
        tiny_evaluate_function = partial(subset_selection.fast_numpy_evaluate_subset,
                                         get_node_semantics=sp.get_node_semantics,
                                         context=pset.context,
                                         subset_selection_archive=tiny_subset_selection_archive,
                                         error_function=toolbox.error_func,
                                         expression_dict=expression_dict)
        mutations = [partial(sp.mutate_single_parametrized_node_optimal, evaluate_function=tiny_evaluate_function,
                             optimization_objective_function=numpy.min),
                     partial(operators.mutation_biased, expr=toolbox.grow, node_selector=toolbox.koza_node_selector)]
        toolbox.register("mutate", mutation.multi_mutation_exclusive, mutations=mutations, probs=[.5, .5])
        toolbox.register("run", afpo.pareto_optimization, population=self.pop, toolbox=toolbox,
                         xover_prob=self.XOVER_PROB, mut_prob=self.MUT_PROB, ngen=self.NGEN,
                         tournament_size=self.TOURNAMENT_SIZE,  num_randoms=self.NUM_RANDOMS, stats=self.mstats,
                         archive=self.multi_archive, calc_pareto_front=False, verbose=False, reevaluate_population=True)
        return toolbox
