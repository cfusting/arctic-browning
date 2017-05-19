import numpy
import random

from deap import gp

from gp.experiments import symbreg


def get_pset(size):
    pset = gp.PrimitiveSet("MAIN", size)
    pset.addPrimitive(numpy.add, 2)
    pset.addPrimitive(numpy.subtract, 2)
    pset.addPrimitive(numpy.multiply, 2)
    pset.addPrimitive(symbreg.numpy_protected_log_abs, 1)
    pset.addPrimitive(numpy.exp, 1)
    pset.addPrimitive(symbreg.cube, 1)
    pset.addPrimitive(numpy.square, 1)
    pset.addEphemeralConstant("gaussian", lambda: random.gauss(0.0, 1.0))
    return pset
