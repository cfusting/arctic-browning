import argparse
import logging
import cachetools

import pygraphviz as pgv
from deap import creator, base

from gp.algorithms import afpo
from ndvi import gp_processing_tools
from gp.parametrized import simple_parametrized_terminals as sp

from utilities import learning_data, lib

parser = argparse.ArgumentParser(description='Plot feature frequency.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory.', required=True)
parser.add_argument('-s', '--seeds', nargs='+', help='List of seeds related to the pareto files to process.')
parser.add_argument('-v', '--verbose', help='Verbose logging.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

experiment = lib.get_experiment(args.experiment)
training_data = learning_data.LearningData()
training_data.from_file(args.training)
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = experiment.get_validation_toolbox(training_data.predictors, training_data.response, pset,
                                                     size_measure=afpo.evaluate_fitness_size_complexity,
                                                     expression_dict=cachetools.LRUCache(maxsize=100),
                                                     fitness_class=creator.ErrorSizeComplexity)
pareto_files = lib.get_pareto_files(args.results, args.experiment, training_data.name)
filtered_files = []
if args.seeds:
    for s in args.seeds:
        filtered_files.extend([x for x in pareto_files if s in x])
else:
    filtered_files = pareto_files
logging.info("Number of pareto files: " + str(len(filtered_files)))
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
        g.graph_attr['K'] = 9
        g.graph_attr['repulsiveforce'] = 3
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="sfdp")
        for j in nodes:
            n = g.get_node(j)
            n.attr["label"] = labels[j]
        g.draw(key + "_tree_" + str(i) + ".svg")
        i += 1
