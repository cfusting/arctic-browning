import logging
from functools import partial
import argparse

import numpy

from gp.experiments import runner

from utilities import learning_data, lib

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-t', '--training', help='Path to the training data as a design matrix in HDF format.',
                    required=True)
parser.add_argument('-s', '--seed', help='Random seed.', required=True, type=int)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-p', '--split', help='Proportion of data used for training.', type=int, default=1)
parser.add_argument('-d', '--debug', help='Debug.', action='store_true')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

experiment = lib.get_experiment(args.experiment)
numpy.seterr(all='ignore')
random_seed = args.seed
training_data = learning_data.LearningData()
training_data.from_csv(args.training)
experiment.SUBSET_SIZE = int(args.split * training_data.num_observations)
transformed_predictors, transformed_response = experiment.transform_features(training_data.predictors,
                                                                             training_data.response)
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
get_toolbox_with_pset = partial(experiment.get_toolbox, pset=pset,
                                variable_type_indices=training_data.variable_type_indices,
                                variable_names=training_data.variable_names)
runner.run_data(random_seed, transformed_predictors, transformed_response, [get_toolbox_with_pset],
                experiment.ALGORITHM_NAMES, dataset_name=training_data.name + "_" + args.experiment,
                logging_level=logging.INFO)
