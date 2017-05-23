import logging
import csv
import glob
import random
import operator
import argparse
import os
import importlib

import cachetools
import numpy
from deap import creator, base
from sklearn import preprocessing

from gp.algorithms import afpo
from gp.experiments import symbreg, fast_evaluate
from ndvi import gp_processing_tools

from utilities import lib

parser = argparse.ArgumentParser(description='Process symbolic regression results.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-j', '--testing', help='Path to testing data as a design matrix in HDF format.', required=True)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory', required=True)
parser.add_argument('-s', '--sample-size', help='Validate and test with a sample of the specified size.', type=int)
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
args = parser.parse_args()

experiment = importlib.import_module("experiments." + args.name)

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)


def get_front(results_path, experiment_name, toolbox, pset):
    """
    Get the pareto front.
    :param results_path:
    :param experiment_name: String
    :param toolbox:
    :param pset:
    :return: A list of individuals.
    """
    logging.info("Reading results from {}".format(results_path))
    pareto_files = glob.glob(results_path + "/pareto_*_po_{}_*.log".format(experiment_name))
    logging.info(len(pareto_files))
    individuals = gp_processing_tools.validate_pareto_optimal_inds(sorted(pareto_files), toolbox, pset=pset)
    logging.info("All individuals from the last pareto fronts = " + str(len(individuals)))
    non_dominated = afpo.find_pareto_front(individuals)
    ft = [individuals[d] for d in non_dominated]
    ft.sort(key=operator.attrgetter("fitness.values"))
    while ft[-1].fitness.values[0] >= 1.0:
        ft.pop()
    ft.reverse()
    return ft

# Validate on a subset of full training data set.
SEED = 123
numpy.random.seed(SEED)
random.seed(SEED)
predictors, response = lib.get_predictors_and_response(args.training)
lst_days, snow_days = lib.get_lst_and_snow_days(args.training)
NUM_DIM = predictors.shape[1]
pset = experiment.get_pset(NUM_DIM, lst_days, snow_days)
p_transformer = preprocessing.StandardScaler()
r_transformer = preprocessing.StandardScaler()
training_predictors = p_transformer.fit_transform(predictors, response)
training_response = r_transformer.fit_transform(response)
if args.sample_size is not None:
    subset_indices = numpy.random.choice(len(training_predictors), args.sample_size, replace=False)
    training_predictors = training_predictors[subset_indices]
    training_response = training_response[subset_indices]
creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = gp_processing_tools.get_toolbox(training_predictors, training_response, pset,
                                                   size_measure=afpo.evaluate_fitness_size_complexity,
                                                   expression_dict=cachetools.LRUCache(maxsize=100),
                                                   fitness_class=creator.ErrorSizeComplexity)

logging.info("Validating models on: " + args.training)
front = get_front(args.results, args.name, validate_toolbox, pset)
with open(os.path.join(args.results, "front_{}_validate_all.txt".format(args.name)), "wb") as f:
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
testing_predictors, testing_response = lib.get_predictors_and_response(args.testing)
testing_predictors = p_transformer.transform(testing_predictors, testing_response)
testing_response = r_transformer.transform(testing_response)
if args.sample_size is not None:
    subset_indices = numpy.random.choice(len(testing_predictors), args.sample_size, replace=False)
    testing_predictors = testing_predictors[subset_indices]
    testing_response = testing_response[subset_indices]
logging.info("Testing models on: " + args.testing)
test_results = []
for individual in front:
    predicted_response = fast_evaluate.fast_numpy_evaluate(individual, pset.context, predictors=testing_predictors,
                                                           expression_dict=None)
    squared_errors = numpy.square(predicted_response - testing_response)
    mse = numpy.mean(squared_errors)
    total_nmse = mse / numpy.var(testing_response)
    test_results.append(total_nmse)

with open(os.path.join(args.results, args.name + "_tests"), 'wb') as test_file:
    writer = csv.writer(test_file)
    writer.writerow(["Error", "Size", "Complexity", "Simplified", "Test Error"])
    for i, ind in enumerate(front):
        rounded_result = "{0:.3f}".format(test_results[i])
        fitness_values = ["{0:.3f}".format(value) for value in ind.fitness.values]
        infix_eq = symbreg.get_infix_equation(ind)
        simplified_equation = symbreg.simplify_infix_equation(infix_eq)
        writer.writerow(fitness_values + [str(len(simplified_equation))] + [rounded_result])
