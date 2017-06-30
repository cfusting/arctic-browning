import argparse
import logging
import re
from functools import partial

from deap import creator

import numpy

from utilities import learning_data, feature as ft, lib


def get_features(feature_file_path, unique_variable_prefixes, pset, validation_toolbox):
    # Most annoyingly this depends on the validation toolbox to have added Individual to the global creator.
        features = []
        exclude = re.compile(r"\de[-|+]?\d")
        with open(feature_file_path) as feature_file:
            i = 0
            for line in feature_file:
                if re.search(exclude, line):
                    continue
                feature = ft.Feature(partial(creator.Individual.from_string, pset=pset),
                                     unique_variable_prefixes)
                feature.from_infix_string(line)
                features.append(feature)
                if i == 100:
                    a = 1
                i += 1
        return features


def build_basis_and_feature_names(features, num_observations, validation_toolbox, response_transformed):
    feature_names = []
    basis = numpy.empty((num_observations, len(features) + 1))
    i = 0
    for feature in features:
        feature_names.append(feature.name)
        basis[:, i] = validation_toolbox.get_semantics(feature.representation)
        i += 1
    feature_names.append('response')
    basis[:, i] = response_transformed
    return basis, feature_names


def change_basis(training_data_path, feature_file_path, output_file_path):
    training_data = learning_data.LearningData()
    training_data.from_file(training_data_path)
    pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                               training_data.variable_names, training_data.variable_dict)
    pset.addPrimitive(numpy.power, 2)
    predictors_transformed, response_transformed = experiment.transform_features(training_data.predictors,
                                                                                 training_data.response)[0:2]
    validation_toolbox = experiment.get_validation_toolbox(predictors_transformed, response_transformed, pset)
    features = get_features(feature_file_path, training_data.unique_variable_prefixes, pset,
                            validation_toolbox)
    basis, feature_names = build_basis_and_feature_names(features, training_data.num_observations, validation_toolbox,
                                                         response_transformed)
    numpy.savetxt(output_file_path, X=basis, delimiter=',', header=','.join(feature_names))


if __name__ == '__main__':
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
    change_basis(args.training, args.features, args.output)

