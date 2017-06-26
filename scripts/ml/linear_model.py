import argparse
import logging

import numpy as np
from sklearn.linear_model import ElasticNetCV, LassoCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import preprocessing

from utilities import learning_data

parser = argparse.ArgumentParser(description='Run ElasticNet.')
parser.add_argument('-t', '--training', help='Path to the training data.', required=True)
parser.add_argument('-j', '--testing', help='Path to the testing data.', required=True)
parser.add_argument('-m', '--method', help='Linear method.', choices=['lasso', 'elasticnet'], default='lasso')
parser.add_argument('-a', '--header', help='Header?', action='store_true')
parser.add_argument('-o', '--output', help='Path to output file.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

training_data = learning_data.LearningData()
training_data.from_file(args.training, header=args.header)
testing_data = learning_data.LearningData()
testing_data.from_file(args.testing, header=args.header)

feature_transformer = preprocessing.StandardScaler()
response_transformer = preprocessing.StandardScaler()

training_predictors_transformed = np.nan_to_num(
    feature_transformer.fit_transform(training_data.predictors, training_data.response))
training_response_transformed = np.nan_to_num(response_transformer.fit_transform(training_data.response))

testing_predictors_transformed = np.nan_to_num(
    feature_transformer.transform(testing_data.predictors, testing_data.response))
testing_response_transformed = np.nan_to_num(response_transformer.transform(testing_data.response))

if args.method == 'elasticnet':
    l1 = [.1, .5, .7, .9, .95, .99, 1]
    method = ElasticNetCV(l1_ratio=l1, cv=10, fit_intercept=False, max_iter=10000)
else:
    method = LassoCV(cv=10, fit_intercept=False, max_iter=10000)
model = method.fit(training_predictors_transformed, training_response_transformed)

coefficients = {}
for i in range(0, len(model.coef_)):
    coefficients[str(training_data.variable_names[i])] = model.coef_[i]
R2 = model.score(training_predictors_transformed, training_response_transformed)
pred_y = model.predict(training_predictors_transformed)
M2 = mean_squared_error(training_response_transformed, pred_y)

t_pred_y = model.predict(testing_predictors_transformed)
t_R2 = r2_score(testing_response_transformed, t_pred_y)
t_M2 = mean_squared_error(testing_response_transformed, t_pred_y)

UM = mean_squared_error(response_transformer.inverse_transform(training_response_transformed),
                        response_transformer.inverse_transform(pred_y))
t_UM = mean_squared_error(response_transformer.inverse_transform(testing_response_transformed),
                          response_transformer.inverse_transform(t_pred_y))

with open(args.output, 'w') as f:
    f.write('Coefficients:\n')
    for key, value in sorted(coefficients.iteritems(), key=lambda (k, v): (v, k)):
        f.write(str(value) + ': ' + str(key) + '\n')
    f.write("Data: R^2, mean square error, untransformed mean squared error" + '\n')
    f.write("Training: {}, {}, {}".format(R2, M2, UM) + '\n')
    f.write("Testing: {}, {}, {}".format(t_R2, t_M2, t_UM) + '\n')