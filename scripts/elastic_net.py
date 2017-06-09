import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import r2_score, mean_squared_error
import sys
from pyhdf.SD import SD, SDC

filename = "../training_matrix.hdf"
testname = "../testing_matrix.hdf"
design = SD(filename, SDC.READ)
test = SD(testname, SDC.READ)

matrix = design.select("design_matrix").get()
test_matrix = test.select("design_matrix").get()

print matrix.shape
print test_matrix.shape
X = matrix[:, 0:-1]
y = matrix[:, -1]
t_X = test_matrix[:, 0:-1]
t_y = test_matrix[:, -1]

l1 = [.1, .5, .7, .9, .95, .99, 1]
enet = ElasticNetCV(l1_ratio=l1, cv=10, fit_intercept=True)
model = enet.fit(X, y)
R2 = model.score(X, y)
pred_y = model.predict(X)
M2 = mean_squared_error(y, pred_y)
t_pred_y = model.predict(t_X)
t_R2 = r2_score(t_y, t_pred_y)
t_M2 = mean_squared_error(t_y, t_pred_y)
print("Data: R^2, mean square error")
print("Training: {}, {}".format(R2, M2))
print("Testing: {}, {}".format(t_R2, t_M2))
