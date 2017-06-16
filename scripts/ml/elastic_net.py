import argparse
import logging

from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import r2_score, mean_squared_error
from pyhdf.SD import SD, SDC
from sklearn import preprocessing

import utilities.learning_data
import utilities.lib
from utilities import lib
from experiments import utils

parser = argparse.ArgumentParser(description='Run ElasticNet.')
parser.add_argument('-t', '--training', help='Path to the training data as a design matrix in HDF format.',
                    required=True)
parser.add_argument('-e', '--testing', help='Path to the testing data as a design matrix in HDF format.',
                    required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

design = SD(args.training, SDC.READ)
test = SD(args.testing, SDC.READ)

matrix = design.select("design_matrix").get()
test_matrix = test.select("design_matrix").get()

logging.debug(matrix.shape)
logging.debug(test_matrix.shape)
training_predictors = matrix[:, 0:-1]
training_response = matrix[:, -1]
testing_predictors = test_matrix[:, 0:-1]
testing_response = test_matrix[:, -1]

feature_transformer = preprocessing.StandardScaler()
response_transformer = preprocessing.StandardScaler()
training_predictors_transformed = feature_transformer.fit_transform(training_predictors, training_response)
training_response_transformed = response_transformer.fit_transform(training_response)
testing_predictors_transformed = feature_transformer.transform(testing_predictors, testing_response)
testing_response_transformed = response_transformer.transform(testing_response)

lst_days, snow_days = utilities.learning_data.get_lst_and_snow_days(args.training)
lst_names = utilities.learning_data.get_lst_names(lst_days)
snow_names = utilities.learning_data.get_snow_names(snow_days)
variable_names = lst_names + snow_names

l1 = [.1, .5, .7, .9, .95, .99, 1]
enet = ElasticNetCV(l1_ratio=l1, cv=10, fit_intercept=True)
model = enet.fit(training_predictors_transformed, training_response_transformed)

logging.info('Coefficients:')
for i in range(0, len(model.coef_)):
    logging.info(str(variable_names[i]) + ': ' + str(model.coef_[i]))

R2 = model.score(training_predictors_transformed, training_response_transformed)
pred_y = model.predict(training_predictors_transformed)
M2 = mean_squared_error(training_response_transformed, pred_y)

t_pred_y = model.predict(testing_predictors_transformed)
t_R2 = r2_score(testing_response_transformed, t_pred_y)
t_M2 = mean_squared_error(testing_response_transformed, t_pred_y)

logging.info("Data: R^2, mean square error")
logging.info("Training: {}, {}".format(R2, M2))
logging.info("Testing: {}, {}".format(t_R2, t_M2))
