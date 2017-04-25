import logging
import operator
import random
from functools import partial
import argparse

import cachetools
import numpy
from deap import creator, base, tools, gp
from sklearn import preprocessing
from pyhdf.SD import SD

from gp.algorithms import afpo, archive, operators, subset_selection
from gp.experiments import runner
from gp.experiments import symbreg, reports, fast_evaluate
from utilities import lib

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-d', '--data', help='Path to data as a design matrix in HDF format.', required=True)
parser.add_argument('-s', '--seed', help='Random seed.', required=True, type=int)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
args = parser.parse_args()

NGEN = 1000
POP_SIZE = 500
TOURNAMENT_SIZE = 2
MIN_DEPTH_INIT = 1
MAX_DEPTH_INIT = 6
MAX_HEIGHT = 17
MAX_SIZE = 200
XOVER_PROB = 0.9
MUT_PROB = 0.1
INTERNAL_NODE_SELECTION_BIAS = 0.9

SUBSET_SIZE = 100000
SUBSET_CHANGE_FREQUENCY = 10

ERROR_FUNCTION = fast_evaluate.normalized_mean_squared_error


def get_archive(pset, toolbox, test_predictors, test_response):
    pareto_archive = archive.ParetoFrontSavingArchive(frequency=100,
                                                      criteria_chooser=archive.
                                                      pick_fitness_size_complexity_from_fitness_age_size_complexity)
    multi_archive = archive.MultiArchive([pareto_archive])
    return multi_archive


def get_toolbox(predictors, response, pset, test_predictors=None, test_response=None):
    creator.create("ErrorAgeSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.ErrorAgeSizeComplexity, age=int)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=MIN_DEPTH_INIT, max_=MAX_DEPTH_INIT)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("select", tools.selRandom)

    toolbox.register("koza_node_selector", operators.internally_biased_node_selector, bias=INTERNAL_NODE_SELECTION_BIAS)
    toolbox.register("mate", operators.one_point_xover_biased, node_selector=toolbox.koza_node_selector)
    toolbox.decorate("mate", operators.static_limit(key=operator.attrgetter("height"), max_value=MAX_HEIGHT))
    toolbox.decorate("mate", operators.static_limit(key=len, max_value=MAX_SIZE))

    toolbox.register("grow", gp.genGrow, pset=pset, min_=1, max_=6)
    toolbox.register("mutate", operators.mutation_biased, expr=toolbox.grow, node_selector=toolbox.koza_node_selector)
    toolbox.decorate("mutate", operators.static_limit(key=operator.attrgetter("height"), max_value=MAX_HEIGHT))
    toolbox.decorate("mutate", operators.static_limit(key=len, max_value=MAX_SIZE))

    expression_dict = cachetools.LRUCache(maxsize=1000)
    subset_selection_archive = subset_selection.RandomSubsetSelectionArchive(frequency=SUBSET_CHANGE_FREQUENCY,
                                                                             predictors=predictors, response=response,
                                                                             subset_size=SUBSET_SIZE,
                                                                             expression_dict=expression_dict)

    toolbox.register("error_func", ERROR_FUNCTION)
    toolbox.register("evaluate_error", subset_selection.fast_numpy_evaluate_subset, context=pset.context,
                     subset_selection_archive=subset_selection_archive,
                     error_function=toolbox.error_func, expression_dict=expression_dict)
    toolbox.register("assign_fitness", afpo.assign_age_fitness_size_complexity)

    multi_archive = get_archive(pset, toolbox, test_predictors, test_response)
    multi_archive.archives.append(subset_selection_archive)
    mstats = reports.configure_inf_protected_stats()

    pop = toolbox.population(n=POP_SIZE)
    toolbox.register("run", afpo.pareto_optimization, population=pop, toolbox=toolbox, xover_prob=XOVER_PROB,
                     mut_prob=MUT_PROB, ngen=NGEN, tournament_size=TOURNAMENT_SIZE, num_randoms=1, stats=mstats,
                     archive=multi_archive, calc_pareto_front=False, verbose=False, reevaluate_population=True)

    toolbox.register("save", reports.save_log_to_csv)
    toolbox.decorate("save", reports.save_archive(multi_archive))

    return toolbox


random_seed = args.seed
predictors, response = lib.get_predictors_and_response(args.data)

pset = gp.PrimitiveSet("MAIN", predictors.shape[1])
pset.addPrimitive(numpy.add, 2)
pset.addPrimitive(numpy.subtract, 2)
pset.addPrimitive(numpy.multiply, 2)
pset.addPrimitive(symbreg.numpy_protected_log_abs, 1)
pset.addPrimitive(numpy.exp, 1)
pset.addPrimitive(symbreg.cube, 1)
pset.addPrimitive(numpy.square, 1)
pset.addEphemeralConstant("gaussian", lambda: random.gauss(0.0, 1.0))

feature_transformer = preprocessing.StandardScaler()
predictors = feature_transformer.fit_transform(predictors, response)
response_transformer = preprocessing.StandardScaler()
response = response_transformer.fit_transform(response)

RANDOM_SUBSET_SIZE = None
if RANDOM_SUBSET_SIZE is not None:
    subset_indices = numpy.random.choice(len(predictors), RANDOM_SUBSET_SIZE, replace=False)
    predictors = predictors[subset_indices]
    response = response[subset_indices]

get_toolbox_with_pset = partial(get_toolbox, pset=pset)
runner.run_data(random_seed, predictors, response, [get_toolbox_with_pset], ["afsc_po"], dataset_name=args.name,
                logging_level=logging.INFO)
