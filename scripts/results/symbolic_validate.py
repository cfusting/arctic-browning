import logging
import csv
import random
import operator
import argparse
import os

import cachetools
import numpy
from deap import creator, base

from utilities import learning_data
from gp.algorithms import afpo
from gp.experiments import symbreg
from ndvi import gp_processing_tools

from utilities import lib

parser = argparse.ArgumentParser(description='Process symbolic regression results.')
parser.add_argument('-t', '--training', help='Path to training data.', required=True)
parser.add_argument('-j', '--testing', help='Path to testing data.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory', required=True)
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
args = parser.parse_args()

experiment = lib.get_experiment(args.experiment)

if args.debug:
    logging.basicConfig(level=logging.DEBUG)


def get_front(results_path, data_set_name, toolbox, pset):
    logging.info("Reading results from {}".format(results_path))
    pareto_files = lib.get_pareto_files(args.results, args.experiment, data_set_name)
    logging.info('Number of files: ' + str(len(pareto_files)))
    for k in pareto_files:
        logging.info(k)
    individuals = gp_processing_tools.validate_pareto_optimal_inds(sorted(pareto_files), toolbox, pset=pset)
    logging.info("All individuals from the last pareto fronts = " + str(len(individuals)))
    non_dominated = afpo.find_pareto_front(individuals)
    ft = [individuals[d] for d in non_dominated]
    ft.sort(key=operator.attrgetter("fitness.values"))
    # while ft[-1].fitness.values[0] >= 1.0:
    #     ft.pop()
    ft.reverse()
    return ft

# Validate on a subset of full training data set.
SEED = 123
numpy.random.seed(SEED)
random.seed(SEED)
training_data = learning_data.LearningData()
training_data.from_file(args.training)
identifier = lib.get_identifier(training_data.name, args.experiment)
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
transformed_predictors, transformed_response, predictor_transformer, response_transformer = \
    experiment.transform_features(training_data.predictors, training_data.response)
creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = experiment.get_validation_toolbox(transformed_predictors, transformed_response, pset,
                                                     size_measure=afpo.evaluate_fitness_size_complexity,
                                                     expression_dict=cachetools.LRUCache(maxsize=100),
                                                     fitness_class=creator.ErrorSizeComplexity)

logging.info("Validating models on: " + args.training)
front = get_front(args.results, training_data.name, validate_toolbox, pset)
with open(os.path.join(args.results, "front_{}_validate_all.txt".format(identifier)), "wb") as f:
    for ind in front:
        logging.info("======================")
        infix_equation = symbreg.get_infix_equation(ind)
        logging.info(infix_equation)
        logging.info("Fitness = " + str(ind.fitness.values))
        logging.info("Training error = " + str(ind.fitness.values))
        logging.info(ind)
        f.write("{}\n".format(ind.fitness.values))
        f.write(str(ind) + "\n")
        logging.info("======================")

# Test
testing_data = learning_data.LearningData()
testing_data.from_file(args.testing)
transformed_testing_predictors, transformed_testing_response = \
    experiment.transform_features(testing_data.predictors, testing_data.response, predictor_transformer,
                                  response_transformer)[0:2]
logging.info("Testing models on: " + args.testing)
testing_toolbox = experiment.get_validation_toolbox(transformed_testing_predictors, transformed_testing_response, pset,
                                                    size_measure=afpo.evaluate_fitness_size_complexity,
                                                    expression_dict=cachetools.LRUCache(maxsize=100),
                                                    fitness_class=creator.ErrorSizeComplexity)
test_results = []
for individual in front:
    test_results.append(testing_toolbox.validate_error(individual)[0])

with open(os.path.join(args.results, identifier + "_tests"), 'wb') as test_file:
    writer = csv.writer(test_file)
    writer.writerow(["Error", "Size", "Complexity", "Simplified", "Test Error"])
    for i, ind in enumerate(front):
        rounded_result = "{0:.3f}".format(test_results[i])
        fitness_values = ["{0:.3f}".format(value) for value in ind.fitness.values]
        infix_eq = symbreg.get_infix_equation(ind)
        simplified_equation = symbreg.simplify_infix_equation(infix_eq)
        writer.writerow(fitness_values + [str(len(simplified_equation))] + [rounded_result])
