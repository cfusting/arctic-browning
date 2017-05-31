import argparse
import logging
import importlib
import cachetools
import glob

import pygraphviz as pgv
from deap import creator, base

from gp.algorithms import afpo
from ndvi import gp_processing_tools
from gp.parametrized import simple_parametrized_terminals as sp

from utilities import lib

parser = argparse.ArgumentParser(description='Plot feature frequency.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory.', required=True)
parser.add_argument('-s', '--seeds', nargs='+', help='List of seeds related to the pareto files to process.')
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

experiment = importlib.import_module("experiments." + args.name)

predictors, response = lib.get_predictors_and_response(args.training)
lst_days, snow_days = lib.get_lst_and_snow_days(args.training)
pset = experiment.get_pset(predictors.shape[1], lst_days, snow_days)
creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = experiment.get_validation_toolbox(predictors, response, pset,
                                                     size_measure=afpo.evaluate_fitness_size_complexity,
                                                     expression_dict=cachetools.LRUCache(maxsize=100),
                                                     fitness_class=creator.ErrorSizeComplexity)
pareto_files = glob.glob(args.results + "/pareto_*_po_{}_*.log".format(args.name))
filtered_files = []
if args.seeds:
    for s in args.seeds:
        filtered_files.extend([x for x in pareto_files if s in x])
else:
    filtered_files = pareto_files
logging.info("Number of pareto files: " +str(len(filtered_files)))
for k in filtered_files:
    logging.info(k)
all_inds = dict()
for f in filtered_files:
    last_front = gp_processing_tools.get_last_pareto_front(f)
    all_inds[f] = []
    for ind_tuple in last_front:
        tree_string = ind_tuple[1]
        pareto_ind = creator.Individual.from_string(tree_string, pset)
        pareto_ind = creator.Individual(pareto_ind)
        all_inds[f].append(pareto_ind)
for key in all_inds.keys():
    i = 0
    for ind in all_inds[key]:
        nodes, edges, labels = sp.graph(ind)
        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")
        for j in nodes:
            n = g.get_node(j)
            n.attr["label"] = labels[j]
        g.draw(key + "_tree_" + str(i) + ".svg")
        i += 1
