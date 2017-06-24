import argparse
import logging
import re
from functools import partial

from deap import creator

import numpy

from utilities import learning_data, feature as ft, lib

parser = argparse.ArgumentParser(description='Change the basis of variables in a data set.')
parser.add_argument('-t', '--training', help='Path to training data.', required=True)
parser.add_argument('-f', '--features', help='Path to feature file.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-o', '--output', help='Path to output file.', required=True)
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
args = parser.parse_args()

experiment = lib.get_experiment(args.experiment)

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

training_data = learning_data.LearningData()
training_data.from_file(args.training)
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
pset.addPrimitive(numpy.power, 2)
predictors_transformed, response_transformed = experiment.transform_features(training_data.predictors,
                                                                             training_data.response)[0:2]
validation_toolbox = experiment.get_validation_toolbox(predictors_transformed, response_transformed, pset)
features = []
exclude = re.compile(r"\de[-|+]?\d")
with open(args.features) as feature_file:
    i = 0
    for line in feature_file:
        if re.search(exclude, line):
            continue
        feature = ft.Feature(partial(creator.Individual.from_string, pset=pset), training_data.variable_prefixes)
        feature.from_infix_string(line)
        features.append(feature)
        i += 1
basis = numpy.empty((training_data.num_observations, len(features) + 1))
feature_names = []
i = 0
for feature in features:
    feature_names.append(feature.name)
    basis[:, i] = validation_toolbox.get_semantics(feature.representation)
    i += 1
feature_names.append('response')
basis[:, i] = response_transformed
numpy.savetxt(args.output, X=basis, delimiter=',', header=','.join(feature_names))
