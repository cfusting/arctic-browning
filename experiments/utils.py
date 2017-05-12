from gp.algorithms import archive


def get_archive():
    pareto_archive = archive.ParetoFrontSavingArchive(frequency=100,
                                                      criteria_chooser=archive.
                                                      pick_fitness_size_complexity_from_fitness_age_size_complexity)
    multi_archive = archive.MultiArchive([pareto_archive])
    return multi_archive


