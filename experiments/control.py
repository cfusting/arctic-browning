import operator
import random

import cachetools
import numpy
from functools import partial

from deap import creator, base, tools, gp

from gp.algorithms import afpo, operators, subset_selection
from gp.experiments import reports, fast_evaluate, symbreg
from gp.parametrized import simple_parametrized_terminals as sp
from gp.algorithms import archive

import utils
import abstract_experiment

NAME = 'Control'


class Control(abstract_experiment.Experiment):

    def __init__(self):
        super(Control, self).__init__()
        self.NGEN = 2000
        self.POP_SIZE = 500
        self.TOURNAMENT_SIZE = 2
        self.MIN_DEPTH_INIT = 1
        self.MAX_DEPTH_INIT = 6
        self.MAX_HEIGHT = 17
        self.MAX_SIZE = 200
        self.XOVER_PROB = 0.9
        self.MUT_PROB = 0.1
        self.INTERNAL_NODE_SELECTION_BIAS = 0.9
        self.MIN_GEN_GROW = 1
        self.MAX_GEN_GROW = 6
        self.SUBSET_SIZE = None
        self.SUBSET_CHANGE_FREQUENCY = 10
        self.ERROR_FUNCTION = fast_evaluate.mean_squared_error
        self.ALGORITHM_NAMES = ["afsc_po"]
        self.NUM_RANDOMS = 1
        self.LOG_MUTATE = False
        self.multi_archive = None
        self.pop = None
        self.mstats = None

    def get_toolbox(self, predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                    test_response=None):
        creator.create("ErrorAgeSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
        creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=creator.ErrorAgeSizeComplexity,
                       age=int)
        toolbox = base.Toolbox()
        toolbox.register("expr", sp.generate_parametrized_expression,
                         partial(gp.genHalfAndHalf, pset=pset, min_=self.MIN_DEPTH_INIT, max_=self.MAX_DEPTH_INIT),
                         variable_type_indices, variable_names)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("compile", gp.compile, pset=pset)
        toolbox.register("select", tools.selRandom)
        toolbox.register("koza_node_selector", operators.internally_biased_node_selector,
                         bias=self.INTERNAL_NODE_SELECTION_BIAS)
        toolbox.register("mate", operators.one_point_xover_biased, node_selector=toolbox.koza_node_selector)
        toolbox.decorate("mate", operators.static_limit(key=operator.attrgetter("height"), max_value=self.MAX_HEIGHT))
        toolbox.decorate("mate", operators.static_limit(key=len, max_value=self.MAX_SIZE))
        toolbox.register("grow", sp.generate_parametrized_expression,
                         partial(gp.genGrow, pset=pset, min_=self.MIN_GEN_GROW, max_=self.MAX_GEN_GROW),
                         variable_type_indices, variable_names)
        toolbox.register("mutate", operators.mutation_biased, expr=toolbox.grow,
                         node_selector=toolbox.koza_node_selector)
        toolbox.decorate("mutate", operators.static_limit(key=operator.attrgetter("height"), max_value=self.MAX_HEIGHT))
        toolbox.decorate("mutate", operators.static_limit(key=len, max_value=self.MAX_SIZE))
        toolbox.register("error_func", self.ERROR_FUNCTION)
        expression_dict = cachetools.LRUCache(maxsize=1000)
        subset_selection_archive = subset_selection.RandomSubsetSelectionArchive(frequency=self.SUBSET_CHANGE_FREQUENCY,
                                                                                 predictors=predictors,
                                                                                 response=response,
                                                                                 subset_size=self.SUBSET_SIZE,
                                                                                 expression_dict=expression_dict)
        evaluate_function = partial(subset_selection.fast_numpy_evaluate_subset,
                                    get_node_semantics=sp.get_node_semantics,
                                    context=pset.context,
                                    subset_selection_archive=subset_selection_archive,
                                    error_function=toolbox.error_func,
                                    expression_dict=expression_dict)
        toolbox.register("evaluate_error", evaluate_function)
        toolbox.register("assign_fitness", afpo.assign_age_fitness_size_complexity)
        self.multi_archive = utils.get_archive()
        if self.LOG_MUTATE:
            mutation_stats_archive = archive.MutationStatsArchive(evaluate_function)
            toolbox.decorate("mutate", operators.stats_collector(archive=mutation_stats_archive))
            self.multi_archive.archives.append(mutation_stats_archive)
        self.multi_archive.archives.append(subset_selection_archive)
        self.mstats = reports.configure_parametrized_inf_protected_stats()
        self.pop = toolbox.population(n=self.POP_SIZE)
        toolbox.register("run", afpo.pareto_optimization, population=self.pop, toolbox=toolbox,
                         xover_prob=self.XOVER_PROB, mut_prob=self.MUT_PROB, ngen=self.NGEN,
                         tournament_size=self.TOURNAMENT_SIZE,  num_randoms=self.NUM_RANDOMS, stats=self.mstats,
                         archive=self.multi_archive, calc_pareto_front=False, verbose=False, reevaluate_population=True)
        toolbox.register("save", reports.save_log_to_csv)
        toolbox.decorate("save", reports.save_archive(self.multi_archive))
        return toolbox

    def get_validation_toolbox(self, predictors, response, pset, size_measure=None, fitness_class=None,
                               expression_dict=None):
        toolbox = base.Toolbox()
        if fitness_class is None:
            creator.create("ErrorSize", base.Fitness, weights=(-1.0, -1.0))
            creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=creator.ErrorSize)
        else:
            creator.create("Individual", sp.SimpleParametrizedPrimitiveTree, fitness=fitness_class)
        toolbox.register("validate_func", partial(self.ERROR_FUNCTION, response=response))
        toolbox.register("validate_error", sp.simple_parametrized_evaluate, context=pset.context, predictors=predictors,
                         error_function=toolbox.validate_func, expression_dict=expression_dict)
        if size_measure is None:
            toolbox.register("validate", afpo.evaluate_fitness_size, error_func=toolbox.validate_error)
        else:
            toolbox.register("validate", size_measure, error_func=toolbox.validate_error)
        return toolbox

    def transform_features(self, predictors, response, predictor_transformer=None, response_transformer=None):
        return predictors, response, None, None

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = sp.SimpleParametrizedPrimitiveSet("MAIN", num_predictors, variable_type_indices, names)
        pset.addPrimitive(numpy.add, 2)
        pset.addPrimitive(numpy.subtract, 2)
        pset.addPrimitive(numpy.multiply, 2)
        pset.addPrimitive(symbreg.numpy_protected_log_abs, 1)
        pset.addPrimitive(numpy.exp, 1)
        pset.addPrimitive(symbreg.cube, 1)
        pset.addPrimitive(numpy.square, 1)
        pset.addEphemeralConstant("gaussian", lambda: random.gauss(0.0, 10.0))
        pset.renameArguments(**variable_dict)
        return pset
