import csv
import logging
import glob
import os
import math
import random
import operator
import argparse
from collections import defaultdict
from functools import partial

import cachetools
import h5py
import numpy
from deap import creator, base
from sklearn import preprocessing

from gp.algorithms import afpo
from gp.experiments import symbreg, reports, fast_evaluate
from ndvi import constants
from ndvi import gp_processing_tools
from utilities import lib

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Process symbolic regression results.')
parser.add_argument('-v', '--validate', help='Path to validation data as a design matrix in HDF format.', required=True)
parser.add_argument('-n', '--name', help='Data set name.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory', required=True)
args = parser.parse_args()


def get_knee(sizes, errors):
    min_size = float(min(sizes))
    max_size = float(max(sizes))
    min_error = min(errors)
    max_error = max(errors)
    min_dist = float("inf")
    solution_index = None

    for i, size in enumerate(sizes):
        size_dist = (sizes[i] - min_size) / (max_size - min_size)
        error_dist = (errors[i] - min_error) / (max_error - min_error)
        dist = math.sqrt(size_dist * size_dist + error_dist * error_dist)

        if dist < min_dist:
            min_dist = dist
            solution_index = i
    return solution_index


def calculate_testing_results(ind, data_dir, context, tile_names, begin_year=2003, end_year=2010):
    test_results = defaultdict(list)
    for year in range(begin_year, end_year + 1):
        print "Testing year {}".format(year)
        testing_predictors_file = os.path.join(data_dir.format(year), "AllX.h5")
        testing_response_file = os.path.join(data_dir.format(year), "AllY.h5")
        testing_indices = os.path.join(data_dir.format(year), "AllIndices.h5")

        indices_file = h5py.File(testing_indices, 'r')
        indices = indices_file["Ind"][:]

        p, r = reports.read_data_from_h5_as_ndarray(testing_predictors_file, testing_response_file)

        for tile in tile_names:
            tile_indices = numpy.where(numpy.core.defchararray.startswith(indices, tile))[0]
            error_func = partial(fast_evaluate.normalized_mean_squared_error, response=r[tile_indices])
            testing_error, = fast_evaluate.fast_numpy_evaluate(ind, context, predictors=p[tile_indices, :],
                                                               error_function=error_func, expression_dict=None)
            test_results[year].append(testing_error)

        error_func = partial(fast_evaluate.normalized_mean_squared_error, response=r)
        testing_error, = fast_evaluate.fast_numpy_evaluate(ind, context, predictors=p,
                                                           error_function=error_func, expression_dict=None)
        test_results[year].append(testing_error)

    return test_results


def normalized_mean_squared_error(vector, response):
    squared_errors = numpy.square(vector - response)
    mse = numpy.mean(squared_errors)
    if not numpy.isfinite(mse):
        return numpy.inf,
    normalized_mse = mse / numpy.var(response)
    return normalized_mse.item(),


def calculate_testing_results_anu(ind, data_dir, context, tile_names, begin_year=2003, end_year=2010):
    test_results = defaultdict(list)
    for year in range(begin_year, end_year + 1):
        print "Testing year {}".format(year)
        testing_predictors_file = os.path.join(data_dir.format(year), "AllX.h5")
        testing_response_file = os.path.join(data_dir.format(year), "AllY.h5")
        testing_indices = os.path.join(data_dir.format(year), "AllIndices.h5")

        indices_file = h5py.File(testing_indices, 'r')
        indices = indices_file["Ind"][:]

        p, r = reports.read_data_from_h5_as_ndarray(testing_predictors_file, testing_response_file)
        predicted_r = fast_evaluate.fast_numpy_evaluate(ind, context, predictors=p, expression_dict=None)
        squared_errors = numpy.square(predicted_r - r)
        mse = numpy.mean(squared_errors)
        total_nmse = mse / numpy.var(r)
        pixel_nmse = squared_errors / numpy.var(r)

        for tile in tile_names:
            tile_indices = numpy.where(numpy.core.defchararray.startswith(indices, tile))[0]
            testing_error = numpy.mean(pixel_nmse[tile_indices])
            test_results[year].append(testing_error)

        test_results[year].append(total_nmse)

    return test_results


def calculate_testing_results_all(inds, data_dir, context, begin_year=2003, end_year=2010, columns=None,
                                  extends_geo_coords=False, feature_transformer=None, response_transformer=None,
                                  elevation_thresholds=None):
    test_results = defaultdict(list)
    for year in range(begin_year, end_year + 1):
        print "Testing year {}".format(year)
        testing_predictors_file = os.path.join(data_dir.format(year), "AllX.h5")
        testing_response_file = os.path.join(data_dir.format(year), "AllY.h5")
        testing_indices = os.path.join(data_dir.format(year), "AllIndices.h5")
        indices = h5py.File(testing_indices)["Ind"][:]

        p, r = reports.read_data_from_h5_as_ndarray(testing_predictors_file, testing_response_file)

        if elevation_thresholds is not None:
            filtered_indices = (elevation_thresholds[0] < p[:, 1]) & (p[:, 1] < elevation_thresholds[1])
            p = p[filtered_indices]
            r = r[filtered_indices]

        if columns is not None:
            p = p[:, columns]

        if extends_geo_coords:
            lon, lat = constants.get_geographic_coordinates(indices, constants.TILE_NAMES_AMAZON,
                                                            constants.NCOLS_AMAZON)
            p = numpy.c_[p, lon, lat]

        if feature_transformer is not None:
            p = feature_transformer.transform(p, r)

        if response_transformer is not None:
            r = response_transformer.transform(r)

        for i, ind in enumerate(inds):
            predicted_r = fast_evaluate.fast_numpy_evaluate(ind, context, predictors=p, expression_dict=None)
            squared_errors = numpy.square(predicted_r - r)
            mse = numpy.mean(squared_errors)
            total_nmse = mse / numpy.var(r)
            test_results[i].append(total_nmse)

    return test_results


def save_testing_results_all(front, results, file_name, begin_year=2003, end_year=2010):
    with open(file_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Error", "Size", "Complexity", "Simplified"] + [str(year) for year in range(begin_year, end_year + 1)]
            + ["Avg testing", "Avg training"])
        for i, ind in enumerate(front):
            rounded_results = ["{0:.3f}".format(a) for a in results[i]]
            rounded_results.append("{0:.3f}".format(numpy.mean(results[i][-3:])))
            rounded_results.append("{0:.3f}".format(numpy.mean(results[i][:5])))
            fitness_values = ["{0:.3f}".format(value) for value in ind.fitness.values]

            infix_eq = symbreg.get_infix_equation(ind)
            simplified_equation = symbreg.simplify_infix_equation(infix_eq)
            writer.writerow(fitness_values + [str(len(simplified_equation))] + rounded_results)

SEED = 123
numpy.random.seed(SEED)
random.seed(SEED)
predictors, response = lib.get_predictors_and_response(args.validate)
NUM_DIM = predictors.shape[1]
pset = symbreg.get_numpy_no_trig_pset(NUM_DIM)
pset.addPrimitive(symbreg.cube, 1)
pset.addPrimitive(numpy.square, 1)

logging.info("Reading results from {}".format(args.results))
pareto_files = glob.glob(args.results + "/pareto_*_po_{}_*.log".format(args.name))
logging.info(len(pareto_files))
p_transformer = preprocessing.StandardScaler()
r_transformer = preprocessing.StandardScaler()
validate_p = p_transformer.fit_transform(predictors, response)
validate_r = r_transformer.fit_transform(response)

RANDOM_SUBSET_SIZE = 100000
subset_indices = numpy.random.choice(len(validate_p), RANDOM_SUBSET_SIZE, replace=False)
validate_p = validate_p[subset_indices]
validate_r = validate_r[subset_indices]

creator.create("ErrorSizeComplexity", base.Fitness, weights=(-1.0, -1.0, -1.0))
validate_toolbox = gp_processing_tools.get_toolbox(validate_p, validate_r, pset,
                                                   size_measure=afpo.evaluate_fitness_size_complexity,
                                                   expression_dict=cachetools.LRUCache(maxsize=100),
                                                   fitness_class=creator.ErrorSizeComplexity)

inds = gp_processing_tools.validate_pareto_optimal_inds(sorted(pareto_files), validate_toolbox, pset=pset)
logging.info("All individuals from the last pareto fronts = " + str(len(inds)))
non_dominated = afpo.find_pareto_front(inds)
front = [inds[i] for i in non_dominated]
front.sort(key=operator.attrgetter("fitness.values"))
while front[-1].fitness.values[0] >= 1.0:
    front.pop()
front.reverse()

with open("front_{}_validate_all.txt".format(args.name), "wb") as f:
    for ind in front:
        logging.info("======================")
        infix_equation = symbreg.get_infix_equation(ind)
        logging.info(infix_equation)
        logging.info("Fitness = " + str(ind.fitness.values))
        logging.info("Training error = " + str(validate_toolbox.validate(ind)))
        logging.info(ind)
        f.write("{}\n".format(ind.fitness.values))
        f.write(str(ind) + "\n")
        logging.info("======================")

"""
testing_results = calculate_testing_results_all(front, testing_data_fold_dir, pset.context,
                                                begin_year=2003, end_year=2010, extends_geo_coords=USE_GEO_COORDS,
                                                feature_transformer=p_transformer, response_transformer=r_transformer,
                                                elevation_thresholds=(30, 500))

save_testing_results_all(front, testing_results,
                         "{}_results_all_validate_all.csv".format(args.name),
                         begin_year=2003, end_year=2010)
"""
