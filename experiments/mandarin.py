import operator
import random
import logging
import math

import cachetools
import numpy
from functools import partial

from gp.parametrized import mutation
from gp.experiments import runner
from deap import creator, base, tools, gp
from gp.algorithms import afpo, operators, subset_selection
from gp.experiments import reports, fast_evaluate, symbreg
from gp.parametrized import simple_parametrized_terminals as sp
from gp.algorithms import archive

import utils

NGEN = 100
POP_SIZE = 50
TOURNAMENT_SIZE = 2
MIN_DEPTH_INIT = 1
MAX_DEPTH_INIT = 6
MAX_HEIGHT = 17
MAX_SIZE = 200
XOVER_PROB = 0
MUT_PROB = 0.8
INTERNAL_NODE_SELECTION_BIAS = 0.9
MIN_GEN_GROW = 1
MAX_GEN_GROW = 6
SUBSET_SIZE = 6
SUBSET_CHANGE_FREQUENCY = 10
ERROR_FUNCTION = fast_evaluate.mean_squared_error
ALGORITHM_NAMES = ["afsc_po"]


def get_toolbox(predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                test_response=None):
    creator.create("ErrorAgeSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
    creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=creator.ErrorAgeSizeComplexity, age=int)
    toolbox = base.Toolbox()
    toolbox.register("expr", sp.generate_parametrized_expression,
                     partial(gp.genHalfAndHalf, pset=pset, min_=MIN_DEPTH_INIT, max_=MAX_DEPTH_INIT),
                     variable_type_indices, variable_names)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("select", tools.selRandom)
    toolbox.register("koza_node_selector", operators.internally_biased_node_selector, bias=INTERNAL_NODE_SELECTION_BIAS)
    toolbox.register("mate", operators.one_point_xover_biased, node_selector=toolbox.koza_node_selector)
    toolbox.decorate("mate", operators.static_limit(key=operator.attrgetter("height"), max_value=MAX_HEIGHT))
    toolbox.decorate("mate", operators.static_limit(key=len, max_value=MAX_SIZE))
    toolbox.register("grow", sp.generate_parametrized_expression,
                     partial(gp.genGrow, pset=pset, min_=MIN_GEN_GROW, max_=MAX_GEN_GROW),
                     variable_type_indices, variable_names)
    mutations = [partial(sp.mutate_single_parametrized_node, stdev_calc=math.sqrt),
                 partial(operators.mutation_biased, expr=toolbox.grow, node_selector=toolbox.koza_node_selector)]
    probs = [.4, .4]
    toolbox.register("mutate", mutation.multi_mutation_exclusive, mutations=mutations, probs=probs)
    toolbox.decorate("mutate", operators.static_limit(key=operator.attrgetter("height"), max_value=MAX_HEIGHT))
    toolbox.decorate("mutate", operators.static_limit(key=len, max_value=MAX_SIZE))
    expression_dict = cachetools.LRUCache(maxsize=1000)
    subset_selection_archive = subset_selection.RandomSubsetSelectionArchive(frequency=SUBSET_CHANGE_FREQUENCY,
                                                                             predictors=predictors, response=response,
                                                                             subset_size=SUBSET_SIZE,
                                                                             expression_dict=expression_dict)
    toolbox.register("error_func", ERROR_FUNCTION)
    evaluate_function = partial(subset_selection.fast_numpy_evaluate_subset,
                                get_node_semantics=sp.get_node_semantics,
                                context=pset.context,
                                subset_selection_archive=subset_selection_archive,
                                error_function=toolbox.error_func,
                                expression_dict=expression_dict)
    mutation_stats_archive = archive.MutationStatsArchive(evaluate_function)
    toolbox.decorate("mutate", operators.stats_collector(archive=mutation_stats_archive))
    toolbox.register("evaluate_error", evaluate_function)
    toolbox.register("assign_fitness", afpo.assign_age_fitness_size_complexity)
    multi_archive = utils.get_archive()
    multi_archive.archives.append(subset_selection_archive)
    multi_archive.archives.append(mutation_stats_archive)
    mstats = reports.configure_parametrized_inf_protected_stats()
    pop = toolbox.population(n=POP_SIZE)
    toolbox.register("run", afpo.pareto_optimization, population=pop, toolbox=toolbox, xover_prob=XOVER_PROB,
                     mut_prob=MUT_PROB, ngen=NGEN, tournament_size=TOURNAMENT_SIZE, num_randoms=1, stats=mstats,
                     archive=multi_archive, calc_pareto_front=False, verbose=False, reevaluate_population=True)
    toolbox.register("save", reports.save_log_to_csv)
    toolbox.decorate("save", reports.save_archive(multi_archive))
    return toolbox


def get_validation_toolbox(predictors, response, pset, size_measure=None, fitness_class=None, expression_dict=None):
    toolbox = base.Toolbox()
    if fitness_class is None:
        creator.create("ErrorSize", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=creator.ErrorSize)
    else:
        creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=fitness_class)
    toolbox.register("validate_func", partial(ERROR_FUNCTION, response=response))
    toolbox.register("validate_error", sp.simple_parametrized_evaluate, context=pset.context, predictors=predictors,
                     error_function=toolbox.validate_func, expression_dict=expression_dict)
    if size_measure is None:
        toolbox.register("validate", afpo.evaluate_fitness_size, error_func=toolbox.validate_error)
    else:
        toolbox.register("validate", size_measure, error_func=toolbox.validate_error)
    return toolbox


def transform_features(predictors, response):
    return utils.transform_features(predictors, response)


def get_pset(num_predictors, variable_type_indices, names):
    pset = sp.SimpleParametrizedPrimitiveSet("MAIN", num_predictors, variable_type_indices, names)
    pset.add_parametrized_terminal(sp.RangeOperationTerminal)
    pset.addPrimitive(numpy.add, 2)
    pset.addPrimitive(numpy.subtract, 2)
    pset.addPrimitive(numpy.multiply, 2)
    pset.addPrimitive(symbreg.numpy_protected_log_abs, 1)
    pset.addPrimitive(numpy.exp, 1)
    pset.addPrimitive(symbreg.cube, 1)
    pset.addPrimitive(numpy.square, 1)
    pset.addEphemeralConstant("gaussian", lambda: random.gauss(0.0, 1.0))
    kwargs = {'ARG0': 'X0', 'ARG1': 'X1', 'ARG2': 'X2', 'ARG3': 'X3', 'ARG4': 'X4'}
    pset.renameArguments(**kwargs)
    return pset


def main():
    random_seed = 2017
    dat = numpy.genfromtxt('/home/cfusting/Dropbox/arctic-browning/analysis/data/construction.csv',
                           delimiter=',', skip_header=True)
    predictors = dat[:, :-1]
    response = dat[:, -1]
    variable_names = ['X0', 'X1', 'X2', 'X3', 'X4']
    variable_type_indices = [4]
    pset = get_pset(5, variable_type_indices, variable_names)
    get_toolbox_with_pset = partial(get_toolbox, pset=pset, variable_type_indices=variable_type_indices,
                                    variable_names=variable_names)
    runner.run_data(random_seed, predictors, response, [get_toolbox_with_pset],
                    ALGORITHM_NAMES, dataset_name='mandarin', logging_level=logging.INFO)

if __name__ == '__main__':
    main()
