from gp.algorithms import archive
from sklearn import preprocessing


def get_archive():
    pareto_archive = archive.ParetoFrontSavingArchive(frequency=1,
                                                      criteria_chooser=archive.
                                                      pick_fitness_size_complexity_from_fitness_age_size_complexity)
    multi_archive = archive.MultiArchive([pareto_archive])
    return multi_archive


def get_lst_names(lst_days):
    return ["lst_" + str(x) for x in lst_days]


def get_snow_names(snow_days):
    return ["snow_" + str(x) for x in snow_days]


def get_variable_names(lst_days, snow_days):
    return get_lst_names(lst_days) + get_snow_names(snow_days)


def get_lst_and_snow_variable_names(lst_days, snow_days):
    lst_args = ["ARG" + str(x) for x in range(0, len(lst_days))]
    lst_names = get_lst_names(lst_days)
    first_args = dict(zip(lst_args, lst_names))
    snow_args = ["ARG" + str(x) for x in range(len(lst_days), len(lst_days) + len(snow_days))]
    snow_names = get_snow_names(snow_days)
    second_args = dict(zip(snow_args, snow_names))
    args = first_args.copy()
    args.update(second_args)
    return args


def get_simple_variable_names(num_vars):
    return ['X' + str(x) for x in range(0, num_vars)]


def get_simple_variable_dict(num_vars):
    args = ['ARG' + str(x) for x in range(0, num_vars)]
    simple = get_simple_variable_names(num_vars)
    return dict(zip(args, simple))


def transform_features(predictors, response):
    feature_transformer = preprocessing.StandardScaler()
    predictors_transformed = feature_transformer.fit_transform(predictors, response)
    response_transformer = preprocessing.StandardScaler()
    response_transformed = response_transformer.fit_transform(response)
    return predictors_transformed, response_transformed


def get_variable_type_indices(lst_days, snow_days):
    return [len(lst_days) - 1, len(lst_days) + len(snow_days) - 1]
