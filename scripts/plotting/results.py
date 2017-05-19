import argparse
import os
import glob
import logging
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import seaborn as sns
import sympy
from deap import creator
from deap import gp, base

from gp.experiments import symbreg
from ndvi import gp_processing_tools

from utilities.gp_lib import get_pset

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory.', required=True)
parser.add_argument('-f', '--feature-number', help='Number of features.', required=True, type=int)
args = parser.parse_args()


def plot_frequent_features(features, feature_counts, feature_performances, num_plotted_features, plot_file,
                           feature_names=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20))
    ax1.set_title("Feature frequency")
    if feature_names is not None:
        for i in range(len(features)):
            for arg in reversed(range(0, len(feature_names))):
                features[i] = features[i].replace("ARG{}".format(arg), feature_names[arg])
    sns.barplot(feature_counts[:num_plotted_features], features[:num_plotted_features], ax=ax1)
    ax2.set_xlim(numpy.min(feature_performances[:num_plotted_features]) - 0.01,
                 numpy.max(feature_performances[:num_plotted_features]) + 0.01)
    ax2.set_title("E(error | feature)")
    sns.barplot(feature_performances[:num_plotted_features], features[:num_plotted_features], ax=ax2)
    plt.savefig(plot_file)


def get_feature_stats(front):
    term_frequency = defaultdict(int)
    term_coefficients = defaultdict(float)
    term_performances = defaultdict(list)
    for ind in front:
        infix_equation = symbreg.get_infix_equation(ind)
        simplified = symbreg.simplify_infix_equation(infix_equation)
        if ind.fitness.values[-1] > 10:
            terms = sympy.expand(simplified, deep=False).as_ordered_terms()
        else:
            terms = sympy.expand(simplified).as_ordered_terms()

        for term in terms:
            coef, t = term.as_coeff_Mul()
            t = str(t)
            if len(t) > 100:
                continue
            if "log" in t or "exp" in t:
                t = symbreg.simplify_logexp_args(t)
            term_frequency[t] += 1
            term_coefficients[t] += coef
            term_performances[t].append(ind.fitness.values[0])

    most_frequent_terms = sorted(term_frequency, key=term_frequency.get, reverse=True)
    for term in most_frequent_terms:
        logging.info("Term : Frequency : Coefficients")
        logging.info("{} : {} : {}".format(term, term_frequency[term], term_coefficients[term]))
    term_counts = [term_frequency[term] for term in most_frequent_terms]
    term_performances = [numpy.mean(term_performances[term]) for term in most_frequent_terms]
    return most_frequent_terms, term_counts, term_performances

FEATURES_NAMES = ["LST_{}".format(x) for x in range(args.feature_number)]

pset = get_pset(args.feature_number)
creator.create("ErrorAgeSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.ErrorAgeSizeComplexity)
pareto_files = glob.glob(args.results + "/pareto_afsc_po_*.log")
logging.debug("Number of pareto files = {}".format(len(pareto_files)))
front = gp_processing_tools.validate_pareto_optimal_inds(pareto_files, pset=pset)
logging.info("Number of pareto front solutions = {}".format(len(front)))
features, counts, performances = get_feature_stats(front)
with open(os.path.join(args.results, "features_{}.txt".format(args.name)), "wb") as f:
    for feature in features:
        f.write("{}\n".format(feature))
plot_frequent_features(features, counts, performances, 51,
                       os.path.join(args.results, "new_features_{}.pdf".format(args.name)), FEATURES_NAMES)
