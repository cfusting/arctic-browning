import csv
import os
import logging
import argparse
import pickle

import numpy
from sklearn import preprocessing

from gp.experiments import symbreg, reports, fast_evaluate
from utilities import lib

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Process symbolic regression on testing data.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-j', '--testing', help='Path to testing data as a design matrix in HDF format.', required=True)
parser.add_argument('-n', '--name', help='Experiment name.', required=True)
parser.add_argument('-r', '--results', help='Path to experiment results directory', required=True)
args = parser.parse_args()

SEED = 123
training_predictors, training_response = lib.get_predictors_and_response(args.training)
p_transformer = preprocessing.StandardScaler()
r_transformer = preprocessing.StandardScaler()
p_transformer.fit(training_predictors, training_response)
r_transformer.fit(training_response)
testing_predictors, testing_response = lib.get_predictors_and_response(args.testing)
testing_predictors = p_transformer.transform(testing_predictors, testing_response)
testing_response = r_transformer.transform(testing_predictors)
front = None
front_file = os.path.join(args.results, args.name + "_front")
with open(front_file, "rb") as pickle_front:
    front = pickle.load(pickle_front)
if front is None:
  sys.exit("Could not find pareto front file: " + front_file)
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
