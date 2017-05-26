import importlib
import logging
from functools import partial
import argparse

import numpy
from sklearn import preprocessing

from gp.experiments import runner
from utilities import lib

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-t', '--training', help='Path to the training data as a design matrix in HDF format.',
                    required=True)
parser.add_argument('-s', '--seed', help='Random seed.', required=True, type=int)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

experiment = importlib.import_module("experiments." + args.name)
numpy.seterr(all='ignore')

random_seed = args.seed
predictors, response = lib.get_predictors_and_response(args.training)
lst_days, snow_days = lib.get_lst_and_snow_days(args.training)
pset = experiment.get_pset(predictors.shape[1], lst_days, snow_days)
feature_transformer = preprocessing.StandardScaler()
predictors = feature_transformer.fit_transform(predictors, response)
response_transformer = preprocessing.StandardScaler()
response = response_transformer.fit_transform(response)
get_toolbox_with_pset = partial(experiment.get_toolbox, pset=pset, lst_days=lst_days, snow_days=snow_days)
runner.run_data(random_seed, predictors, response, [get_toolbox_with_pset], experiment.ALGORITHM_NAMES,
                dataset_name=args.name, logging_level=logging.INFO)
