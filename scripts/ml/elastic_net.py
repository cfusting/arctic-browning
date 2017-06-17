import argparse
import logging

from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import preprocessing

from utilities import learning_data
import utilities.lib

parser = argparse.ArgumentParser(description='Run ElasticNet.')
parser.add_argument('-t', '--training', help='Path to the training data.', required=True)
parser.add_argument('-e', '--testing', help='Path to the testing data.', required=True)
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

training_data = learning_data.LearningData()
training_data.from_file(args.training)
testing_data = learning_data.LearningData()
testing_data.from_file(args.training)

feature_transformer = preprocessing.StandardScaler()
response_transformer = preprocessing.StandardScaler()
training_predictors_transformed = feature_transformer.fit_transform(training_data.predictors, training_data.response)
training_response_transformed = response_transformer.fit_transform(training_data.response)
testing_predictors_transformed = feature_transformer.transform(testing_data.predictors, testing_data.response)
testing_response_transformed = response_transformer.transform(testing_data.response)

l1 = [.1, .5, .7, .9, .95, .99, 1]
enet = ElasticNetCV(l1_ratio=l1, cv=10, fit_intercept=True)
model = enet.fit(training_predictors_transformed, training_response_transformed)

logging.info('Coefficients:')
for i in range(0, len(model.coef_)):
    logging.info(str(training_data.variable_names[i]) + ': ' + str(model.coef_[i]))

R2 = model.score(training_predictors_transformed, training_response_transformed)
pred_y = model.predict(training_predictors_transformed)
M2 = mean_squared_error(training_response_transformed, pred_y)

t_pred_y = model.predict(testing_predictors_transformed)
t_R2 = r2_score(testing_response_transformed, t_pred_y)
t_M2 = mean_squared_error(testing_response_transformed, t_pred_y)

logging.info("Data: R^2, mean square error")
logging.info("Training: {}, {}".format(R2, M2))
logging.info("Testing: {}, {}".format(t_R2, t_M2))
