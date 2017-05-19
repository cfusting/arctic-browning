from gp.algorithms import archive


def get_archive():
    pareto_archive = archive.ParetoFrontSavingArchive(frequency=100,
                                                      criteria_chooser=archive.
                                                      pick_fitness_size_complexity_from_fitness_age_size_complexity)
    multi_archive = archive.MultiArchive([pareto_archive])
    return multi_archive


def get_lst_and_snow_variable_names(lst_days, snow_days):
    lst_args = ["ARG" + str(x) for x in range(0, len(lst_days))]
    lst_names = ["lst_" + str(x) for x in lst_days]
    first_args = dict(zip(lst_args, lst_names))
    snow_args = ["ARG" + str(x) for x in range(len(lst_days), len(lst_days) + len(snow_days))]
    snow_names = ["snow_" + str(x) for x in lst_days]
    second_args = dict(zip(snow_args, snow_names))
    args = first_args.copy()
    args.update(second_args)
    return args
