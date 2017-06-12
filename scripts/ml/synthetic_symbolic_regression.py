import argparse
import logging
import importlib
from functools import partial
import ntpath

import numpy

from gp.experiments import runner
from gp.parametrized import simple_parametrized_terminals as sp

from experiments import utils

parser = argparse.ArgumentParser(description='Run simple symbolic regression.')
parser.add_argument('-t', '--training', help='Path to the training data as a design matrix in CSV format.',
                    required=True)
parser.add_argument('-s', '--seed', help='Random seed.', required=True, type=int)
parser.add_argument('-n', '--name', help='Experiment name.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

experiment = importlib.import_module("experiments." + args.name)
numpy.seterr(all='ignore')

random_seed = args.seed
dat = numpy.genfromtxt(args.training, delimiter=',', skip_header=True)
predictors = dat[:, :-1]
response = dat[:, -1]
num_rows, num_columns = predictors.shape
experiment.SUBSET_SIZE = num_rows
num_vars = num_columns
variable_names = utils.get_simple_variable_names(num_vars)
transformed_predictors, transformed_response = utils.transform_features(predictors, response)
variable_type_indices = [num_vars - 1]
pset = experiment.get_pset(num_vars, variable_type_indices, variable_names)
get_toolbox_with_pset = partial(experiment.get_toolbox, pset=pset, variable_type_indices=variable_type_indices,
                                variable_names=variable_names)
tree = 'RangeOperation(sum,X0,X5)'
paramtree = sp.SimpleParametrizedPrimitiveTree.from_string(tree, pset)
res = sp.simple_parametrized_evaluate(paramtree, pset.context, transformed_predictors,
                                      error_function=partial(experiment.ERROR_FUNCTION, response=transformed_response))
experiment_name = ntpath.basename(args.training)[:-4] + "_" + args.name
runner.run_data(random_seed, transformed_predictors, transformed_response, [get_toolbox_with_pset],
                experiment.ALGORITHM_NAMES, dataset_name=experiment_name,
                logging_level=logging.INFO)
