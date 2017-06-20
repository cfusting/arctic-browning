import argparse
import logging
import cachetools
import os.path

import pygraphviz as pgv
from deap import creator, base

from gp.algorithms import afpo
from gp.parametrized import simple_parametrized_terminals as sp

from utilities import learning_data, lib

parser = argparse.ArgumentParser(description='Plot feature frequency.')
parser.add_argument('-t', '--training', help='Path to training data as a design matrix in HDF format.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-f', '--file', help='Path to pareto fronts file.', required=True)
parser.add_argument('-d', '--debug', help='Debug logging.', action='store_true')
args = parser.parse_args()

if args.debug:
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
individuals = []
with open(args.file, 'r') as f:
    count = 0
    for line in f:
        count += 1
        if count % 2 == 0:
            pareto_ind = creator.Individual.from_string(line, pset)
            pareto_ind = creator.Individual(pareto_ind)
            individuals.append(pareto_ind)
path = os.path.abspath(os.path.join(args.file, os.pardir))
for index, ind in enumerate(individuals):
    nodes, edges, labels = sp.graph(ind)
    g = pgv.AGraph()
    #g.graph_attr['K'] = 1
    g.node_attr['nodesep'] = '1'
    g.node_attr['ranksep'] = '1'
    #g.graph_attr['repulsiveforce'] = 3
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="neato")
    for j in nodes:
        n = g.get_node(j)
        n.attr["label"] = labels[j]
    g.draw(path=str(path) + os.sep + str(index) + '_pareto_individual' + '.svg')
