import logging
import csv
import glob
import random
import operator
import argparse
import os
import pickle

import cachetools
import numpy
from deap import creator, base
from sklearn import preprocessing

from gp.algorithms import afpo
from gp.experiments import symbreg, fast_evaluate
from ndvi import gp_processing_tools
from utilities import lib

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Process symbolic regression results.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory', required=True)
args = parser.parse_args()


def get_front(results_path, experiment_name, toolbox, primitive_set):
    logging.info("Reading results from {}".format(results_path))
    pareto_files = glob.glob(results_path + "/pareto_*_po_{}_*.log".format(experiment_name))
    logging.info(len(pareto_files))
    individuals = gp_processing_tools.validate_pareto_optimal_inds(sorted(pareto_files), toolbox, pset=primitive_set)
    logging.info("All individuals from the last pareto fronts = " + str(len(individuals)))
    non_dominated = afpo.find_pareto_front(individuals)
    front = [individuals[i] for i in non_dominated]
    front.sort(key=operator.attrgetter("fitness.values"))
    while front[-1].fitness.values[0] >= 1.0:
        front.pop()
    front.reverse()
    return front

# Validate
SEED = 123
numpy.random.seed(SEED)
random.seed(SEED)
predictors, response = lib.get_predictors_and_response(args.training)
NUM_DIM = predictors.shape[1]
pset = lib.get_validation_testing_pset(NUM_DIM)
p_transformer = preprocessing.StandardScaler()
r_transformer = preprocessing.StandardScaler()
validate_p = p_transformer.fit_transform(predictors, response)
validate_r = r_transformer.fit_transform(response)

creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = gp_processing_tools.get_toolbox(validate_p, validate_r, pset,
                                                   size_measure=afpo.evaluate_fitness_size_complexity,
                                                   expression_dict=cachetools.LRUCache(maxsize=100),
                                                   fitness_class=creator.ErrorSizeComplexity)
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
testing_response = r_transformer.transform(testing_predictors)
context = lib.get_validation_testing_pset(testing_predictors.shape[1]).context
test_results = []
for i, individual in enumerate(front):
    predicted_r = fast_evaluate.fast_numpy_evaluate(individual, context, predictors=testing_predictors,
                                                    expression_dict=None)
    squared_errors = numpy.square(predicted_r - testing_response)
    mse = numpy.mean(squared_errors)
    total_nmse = mse / numpy.var(testing_response)
    test_results.append(total_nmse)

with open(os.path.join(args.results, args.name + "_tests", 'wb')) as test_file:
    writer = csv.writer(test_file)
    writer.writerow(["Error", "Size", "Complexity", "Simplified", "Test Error"])
    for i, ind in front:
        rounded_results = ["{0:.3f}".format(a) for a in test_results[i]]
        fitness_values = ["{0:.3f}".format(value) for value in ind.fitness.values]
        infix_eq = symbreg.get_infix_equation(ind)
        simplified_equation = symbreg.simplify_infix_equation(infix_eq)
        writer.writerow(fitness_values + [str(len(simplified_equation))] + rounded_results)
