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
args = parser.parse_args()
ferret = importlib.import_module("experiments", args.name)
logging.basicConfig(level=logging.DEBUG)
numpy.seterr(all='ignore')
RANDOM_SUBSET_SIZE = 100000
random_seed = args.seed
predictors, response = lib.get_predictors_and_response(args.training)
pset = ferret.get_pset(predictors.shape[1])
feature_transformer = preprocessing.StandardScaler()
predictors = feature_transformer.fit_transform(predictors, response)
response_transformer = preprocessing.StandardScaler()
response = response_transformer.fit_transform(response)
if RANDOM_SUBSET_SIZE is not None:
    subset_indices = numpy.random.choice(len(predictors), RANDOM_SUBSET_SIZE, replace=False)
    predictors = predictors[subset_indices]
    response = response[subset_indices]
get_toolbox_with_pset = partial(ferret.get_toolbox, pset=pset)
runner.run_data(random_seed, predictors, response, [get_toolbox_with_pset], ["afsc_po"], dataset_name=args.name,
                logging_level=logging.INFO)
