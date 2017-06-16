from sklearn import preprocessing

from gp.algorithms import archive


def get_archive():
    pareto_archive = archive.ParetoFrontSavingArchive(frequency=1,
                                                      criteria_chooser=archive.
                                                      pick_fitness_size_complexity_from_fitness_age_size_complexity)
    multi_archive = archive.MultiArchive([pareto_archive])
    return multi_archive


def transform_features(predictors, response):
    feature_transformer = preprocessing.StandardScaler()
    predictors_transformed = feature_transformer.fit_transform(predictors, response)
    response_transformer = preprocessing.StandardScaler()
    response_transformed = response_transformer.fit_transform(response)
    return predictors_transformed, response_transformed


