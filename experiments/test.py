from gp.parametrized import simple_parametrized_terminals as sp
import math
from deap import gp
import numpy as np
from functools import partial
from copy import deepcopy


def get_pset(num_predictors, variable_type_indices, names):
    pset = sp.SimpleParametrizedPrimitiveSet("MAIN", num_predictors, variable_type_indices, names)
    pset.add_parametrized_terminal(sp.RangeOperationTerminal)
    kwargs = {'ARG0': 'X0', 'ARG1': 'X1', 'ARG2': 'X2', 'ARG3': 'X3', 'ARG4': 'X4'}
    pset.renameArguments(**kwargs)
    return pset

random_seed = 2017
dat = np.genfromtxt('/home/cfusting/Dropbox/arctic-browning/analysis/data/construction.csv',
                   delimiter=',', skip_header=True)
predictors = dat[:, :-1]
response = dat[:, -1]
variable_names = ['X0', 'X1', 'X2', 'X3', 'X4']
variable_type_indices = [4]
pset = get_pset(0, variable_type_indices, variable_names)
pset.addPrimitive(np.add, 2)
pset.add_parametrized_terminal(sp.RangeOperationTerminal)
expr = sp.generate_parametrized_expression(partial(gp.genFull, pset=pset, min_=2, max_=2), variable_type_indices,
                                           variable_names)
tree = sp.SimpleParametrizedPrimitiveTree(expr)

print(tree)
tree2 = deepcopy(tree)
sp.mutate_parametrized_nodes(tree2, math.sqrt)
print(tree)
print(tree2)

# print(sp.simple_parametrized_evaluate(tree, pset.context, predictors))
