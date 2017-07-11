import logging
import os
import csv
import random
import operator
import argparse

import cachetools
import numpy
from deap import creator, base

from utilities import learning_data
from gp.algorithms import afpo
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


def get_fronts(results_path, data_set_name, toolbox, pset):
    logging.info("Reading results from {}".format(results_path))
    pareto_files = lib.get_pareto_files(args.results, args.experiment, data_set_name)
    logging.info('Number of files: ' + str(len(pareto_files)))
    all_fronts = []
    for k in pareto_files:
        current_front = []
        raw_front = gp_processing_tools.get_last_pareto_front(k)
        for ind_tuple in raw_front:
            tree_string = ind_tuple[1]
            pareto_ind = creator.Individual.from_string(tree_string, pset)
            pareto_ind = creator.Individual(pareto_ind)
            pareto_ind.fitness.values = toolbox.validate(pareto_ind)
            current_front.append(pareto_ind)
        current_front.sort(key=operator.attrgetter("fitness.values"))
        current_front.reverse()
        all_fronts.append(current_front)
    return all_fronts

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
fronts = get_fronts(args.results, training_data.name, validate_toolbox, pset)

# Test
testing_data = learning_data.LearningData()
testing_data.from_file(args.testing)
transformed_testing_predictors, transformed_testing_response = \
    experiment.transform_features(testing_data.predictors, testing_data.response, predictor_transformer,
                                  response_transformer)[0:2]
testing_toolbox = experiment.get_validation_toolbox(transformed_testing_predictors, transformed_testing_response, pset,
                                                    size_measure=afpo.evaluate_fitness_size_complexity,
                                                    expression_dict=cachetools.LRUCache(maxsize=100),
                                                    fitness_class=creator.ErrorSizeComplexity)
test_results = []
for front in fronts:
    front_results = []
    for individual in front:
        front_results.append(testing_toolbox.validate_error(individual)[0])
    test_results.append(front_results)

average_validation = map(lambda x: numpy.mean([y.fitness.values[0] for y in x]), fronts)
average_size = map(lambda x: numpy.mean([y.fitness.values[1] for y in x]), fronts)
average_complexity = map(lambda x: numpy.mean([y.fitness.values[2] for y in x]), fronts)
average_test = map(lambda x: numpy.mean(x), test_results)

with open(os.path.join(args.results, identifier + "_run_statistics"), 'wb') as test_file:
    writer = csv.writer(test_file)
    writer.writerow(["average_validation", "average_size", "average_complexity", "average_test"])
    for i in range(0, len(fronts)):
        writer.writerow([str(average_validation[i]),
                         str(average_size[i]),
                         str(average_complexity[i]),
                         str(average_test[i])])


def get_best_validation_and_corresponding_test(front_array, test_array):
    min_validations = []
    tests = []
    for j in range(0, len(front_array)):
        validation_array = [x.fitness.values[0] for x in front_array[j]]
        min_validation = min(validation_array)
        min_index = validation_array.index(min_validation)
        min_validations.append(min_validation)
        tests.append(test_array[j][min_index])
    return min_validations, tests


average_best_validation, average_corresponding_test = get_best_validation_and_corresponding_test(fronts, test_results)
with open(os.path.join(args.results, identifier + "_best_validation"), 'wb') as test_file:
    writer = csv.writer(test_file)
    writer.writerow(["best_validation", "test_error"])
    for i in range(0, len(average_best_validation)):
        writer.writerow([str(average_best_validation[i]), str(average_corresponding_test[i])])
