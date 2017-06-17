import argparse
import os
import logging
import importlib
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import seaborn as sns
import sympy

from utilities import learning_data, lib
from gp.experiments import symbreg
from ndvi import gp_processing_tools


parser = argparse.ArgumentParser(description='Plot feature frequency.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
args = parser.parse_args()

experiment = lib.get_experiment(args.experiment)

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)


def plot_frequent_features(feats, feature_counts, feature_performances, num_plotted_features, plot_file,
                           feature_names=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20))
    ax1.set_title("Feature frequency")
    if feature_names is not None:
        for i in range(len(feats)):
            for arg in reversed(range(0, len(feature_names))):
                feats[i] = feats[i].replace("ARG{}".format(arg), feature_names[arg])
    sns.barplot(feature_counts[:num_plotted_features], feats[:num_plotted_features], ax=ax1)
    ax2.set_xlim(numpy.min(feature_performances[:num_plotted_features]) - 0.01,
                 numpy.max(feature_performances[:num_plotted_features]) + 0.01)
    ax2.set_title("E(error | feature)")
    sns.barplot(feature_performances[:num_plotted_features], feats[:num_plotted_features], ax=ax2)
    plt.savefig(plot_file)


def get_feature_stats(ft):
    term_frequency = defaultdict(int)
    term_coefficients = defaultdict(float)
    term_performances = defaultdict(list)
    for ind in ft:
        infix_equation = symbreg.get_infix_equation(ind)
        logging.debug("Got infix equation for individual: " + str(infix_equation))
        if str(infix_equation) == 'exp((((log(-0.05739)) ^ 3) ^ 3) ^ 3)':
            continue
        elif str(infix_equation) == '((0.12148 * (((0.12148 * (((X50 - X10) + X15) + (((X42 - X6) + ((X33 + X36) + ((X9 - X7) + (X51 - X19)))) + X58))) + ((X58) ^ 2)) + ((0.44711 * X58) ^ 3))) ^ 3) ^ 3':
            continue
        simplified = symbreg.simplify_infix_equation(infix_equation)
        logging.debug("Got simplified equation for individual: " + str(simplified))
        if ind.fitness.values[-1] > 10:
            terms = sympy.expand(simplified, deep=False).as_ordered_terms()
        else:
            terms = sympy.expand(simplified).as_ordered_terms()

        for term in terms:
            logging.debug("Looking at term: " + str(term))
            coef, t = term.as_coeff_Mul()
            t = str(t)
            if len(t) > 100:
                continue
            if "log" in t or "exp" in t:
                t = symbreg.simplify_logexp_args(t)
            term_frequency[t] += 1
            logging.debug("Added count for feature: " + str(t))
            term_coefficients[t] += coef
            logging.debug("Added count for coefficient : " + str(coef))
            term_performances[t].append(ind.fitness.values[0])
            logging.debug("Added feature performance: " + str(ind.fitness.values[0]))

    most_frequent_terms = sorted(term_frequency, key=term_frequency.get, reverse=True)
    for term in most_frequent_terms:
        logging.info("Term : Frequency : Coefficients")
        logging.info("{} : {} : {}".format(term, term_frequency[term], term_coefficients[term]))
    term_counts = [term_frequency[term] for term in most_frequent_terms]
    term_performances = [numpy.mean(term_performances[term]) for term in most_frequent_terms]
    return most_frequent_terms, term_counts, term_performances

training_data = learning_data.LearningData()
training_data.from_file(args.training)
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
predictors_transformed, response_transformed = experiment.transform_features(training_data.predictors,
                                                                             training_data.response)
pareto_files = lib.get_pareto_files(args.results, args.experiment, args.name)
logging.info("Number of pareto files = {}".format(len(pareto_files)))
validation_toolbox = experiment.get_validation_toolbox(predictors_transformed, response_transformed, pset)
front = gp_processing_tools.validate_pareto_optimal_inds(pareto_files, pset=pset, toolbox=validation_toolbox)
logging.info("Number of pareto front solutions = {}".format(len(front)))
features, counts, performances = get_feature_stats(front)
identifier = args.experiment + '_' + args.name
with open(os.path.join(args.results, "features_{}.txt".format(identifier)), "wb") as f:
    for feature in features:
        f.write("{}\n".format(feature))
plot_frequent_features(features, counts, performances, 51,
                       os.path.join(args.results, "new_features_{}.pdf".format(identifier)))
