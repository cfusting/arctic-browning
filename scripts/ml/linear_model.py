import argparse
import math
import gc
import logging

import numpy as np
from sklearn.linear_model import ElasticNetCV, LassoCV, Lasso
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import preprocessing

from utilities import learning_data

parser = argparse.ArgumentParser(description='Run ElasticNet.')
parser.add_argument('-t', '--training', help='Path to the training data.', required=True)
parser.add_argument('-j', '--testing', help='Path to the testing data.', required=True)
parser.add_argument('-m', '--method', help='Linear method.', choices=['lasso', 'elasticnet', 'alpha'], default='lasso')
parser.add_argument('-a', '--alpha', help='Alpha value (if using method alpha).', type=int)
parser.add_argument('-n', '--normalize', help='Normalize Data.', action='store_true')
parser.add_argument('-s', '--standardize', help='Standardize Data.', action='store_true')
parser.add_argument('-o', '--output', help='Path to output file.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

if args.standardize and args.normalize:
    logging.warning("You probably don't want to standardize AND normalize the data...")

training_data = learning_data.LearningData()
training_data.from_file(args.training)
testing_data = learning_data.LearningData()
testing_data.from_file(args.testing)
variable_names = training_data.variable_names

training_predictors = training_data.predictors
training_response = training_data.response
del training_data
gc.collect()

testing_predictors = testing_data.predictors
testing_response = testing_data.response
del testing_data
gc.collect()

feature_transformer = preprocessing.StandardScaler()
response_transformer = preprocessing.StandardScaler()

if args.standardize:
    training_predictors = np.nan_to_num(feature_transformer.fit_transform(training_predictors, training_response))
    training_response = np.nan_to_num(response_transformer.fit_transform(training_response))
    testing_predictors = np.nan_to_num(feature_transformer.transform(testing_predictors, testing_response))
    testing_response = np.nan_to_num(response_transformer.transform(testing_response))

logging.info("Building linear model.")
if args.method == 'elasticnet':
    l1 = [.1, .5, .7, .9, .95, .99, 1]
    method = ElasticNetCV(l1_ratio=l1, cv=10, fit_intercept=True, max_iter=100000, normalize=args.normalize)
elif args.method == 'lasso':
    method = LassoCV(cv=10, fit_intercept=True, max_iter=100000, normalize=args.normalize)
else:
    method = Lasso(alpha=args.alpha, fit_intercept=False, normalize=args.normalize)
model = method.fit(training_predictors, training_response)

coefficients = {}
for i in range(0, len(model.coef_)):
    coefficients[str(variable_names[i])] = model.coef_[i]
R2 = model.score(training_predictors, training_response)
pred_y = model.predict(training_predictors)
M2 = mean_squared_error(training_response, pred_y)

t_pred_y = model.predict(testing_predictors)
t_R2 = r2_score(testing_response, t_pred_y)
t_M2 = mean_squared_error(testing_response, t_pred_y)

UM = 0
t_UM = 0
if args.standardize:
    UM = mean_squared_error(response_transformer.inverse_transform(training_response),
                            response_transformer.inverse_transform(pred_y))
    t_UM = mean_squared_error(response_transformer.inverse_transform(testing_response),
                              response_transformer.inverse_transform(t_pred_y))

standardized = ''
normalized = ''
if args.standardize:
    standardized = 'standardized'
if args.normalize:
    normalized = 'normalized'
if not args.alpha:
    args.alpha = ''
file_name = '_'.join([args.output, args.method, args.alpha, standardized, normalized])
with open(file_name, 'w') as f:
    f.write('Chosen alpha: ' + str(method.alpha_) + '\n')
    f.write('Alphas used: ' + str(method.alphas_) + '\n')
    f.write('MSE on alpha, fold: ' + str(method.mse_path_) + '\n')
    f.write('Coefficients:\n')
    for key, value in sorted(coefficients.iteritems(), key=lambda (k, v): (v, k)):
        f.write(str(value) + ': ' + str(key) + '\n')
    f.write("Data: R^2, mean square error, untransformed mean squared error, untransformed mean error" + '\n')
    f.write("Training: {}, {}, {}, {}".format(R2, M2, UM, math.sqrt(UM)) + '\n')
    f.write("Testing: {}, {}, {}, {}".format(t_R2, t_M2, t_UM, math.sqrt(t_UM)) + '\n')
