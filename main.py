import json
import math
import os

from pyswaro import cdta_algo, novel_algo_ring, novel_algo_star, radar_algo


def create_dir_and_visit(name):
    target_dir = os.path.join(os.getcwd(), name)
    os.mkdir(target_dir)
    os.chdir(target_dir)


def go_back():
    os.chdir("..")


def change_params(params):
    json_params = json.dumps(params, indent=4)
    with open("vars.json", "w") as outfile:
        outfile.write(json_params)


def run_experiment(experiment_name, params, annotations=True):
    create_dir_and_visit(experiment_name)
    change_params(params)
    radar_algo(annots=annotations)
    go_back()


def run_experiment_simplified_star(experiment_name, params, annotations=True):
    create_dir_and_visit(experiment_name)
    change_params(params)
    novel_algo_star(annots=annotations)
    go_back()


def run_experiment_simplified_ring(experiment_name, params, annotations=True):
    create_dir_and_visit(experiment_name)
    change_params(params)
    novel_algo_ring(annots=annotations)
    go_back()


def run_cdta(experiment_name, params, annotations=True):
    create_dir_and_visit(experiment_name)
    change_params(params)
    cdta_algo(annots=annotations)
    go_back()


def experiment_xyz():
    params = {
        "ROWS": 10,
        "COLS": 10,
        "MIN_INIT_BATTERY": 60,
        "MAX_INIT_BATTERY": 100,
        "MIN_OPERABLE_BATTERY": 2,
        "MAX_RANGE": 5,
        "BATTERY_TOLLS": {
            'COMMUNICATION': 5e-4,
            'MOVEMENT': 6e-4,
            'ALREADY_VISITED': 2.5e-4,
        },
        "TIME_TOLLS": {
            'SCAN': 2e-3,
            'TIMEOUT': 1e-3,
            'PER_RANGE': 0.5e-3,
            'LEFTOVER': 3e-3,
            'ALREADY_VISITED': 1e-3,
            'LEADER_TO_LEADER': 1e-3
        },

        "LEADERS_COORDINATES": [(0, 0), (0, 9), (9, 0), (9, 9), (4, 4)]
    }

    annots = params["ROWS"] <= 30 and params["COLS"] <= 30
    run_experiment("experiment_xyz", params, annotations=annots)


def cdta():
    params = {
        "ROWS": 6,
        "COLS": 6,
        "MIN_INIT_BATTERY": 60,
        "MAX_INIT_BATTERY": 100,
        "MIN_OPERABLE_BATTERY": 2,
        "MAX_RANGE": -1,
        "BATTERY_TOLLS": {
            'COMMUNICATION': 5e-4,
        },
        "TIME_TOLLS": {
            'COMMUNICATION': 1e-3,
            'LEADER_TO_LEADER': 1e-3
        },

        # "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        # allocate a rectangle from 2 edge coordinates
        "LEADERS_DOMAIN": [[(0, 0), (2, 2)], [(0, 3), (2, 5)], [(3, 0), (5, 2)], [(3, 3), (5, 5)]]
    }

    annots = params["ROWS"] <= 30 and params["COLS"] <= 30
    run_cdta("cdta", params, annotations=annots)


def our_star_approach():
    params = {
        "ROWS": 6,
        "COLS": 6,
        "MIN_INIT_BATTERY": 60,
        "MAX_INIT_BATTERY": 100,
        "MIN_OPERABLE_BATTERY": 2,
        "MAX_RANGE": -1,
        "BATTERY_TOLLS": {
            'COMMUNICATION': 5e-4,
        },
        "TIME_TOLLS": {
            'COMMUNICATION': 1e-3,
            'LEADER_TO_LEADER': 1e-3
        },

        # "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        # allocate a rectangle from 2 edge coordinates
        "LEADERS_DOMAIN": [[(0, 0), (2, 2)], [(0, 3), (2, 5)], [(3, 0), (5, 2)], [(3, 3), (5, 5)]]
    }

    annots = params["ROWS"] <= 30 and params["COLS"] <= 30
    run_experiment_simplified_star(
        "our_star_approach", params, annotations=annots)


def our_ring_approach():
    params = {
        "ROWS": 6,
        "COLS": 6,
        "MIN_INIT_BATTERY": 60,
        "MAX_INIT_BATTERY": 100,
        "MIN_OPERABLE_BATTERY": 2,
        "MAX_RANGE": -1,
        "BATTERY_TOLLS": {
            'COMMUNICATION': 5e-4,
        },
        "TIME_TOLLS": {
            'COMMUNICATION': 1e-3,
            'LEADER_TO_LEADER': 1e-3
        },

        # "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)],
        # allocate a rectangle from 2 edge coordinates
        "LEADERS_DOMAIN": [[(0, 0), (2, 2)], [(0, 3), (2, 5)], [(3, 0), (5, 2)], [(3, 3), (5, 5)]]
    }

    annots = params["ROWS"] <= 30 and params["COLS"] <= 30
    run_experiment_simplified_ring(
        "our_ring_approach", params, annotations=annots)


def original_radar():
    params = {
        "ROWS": 6,
        "COLS": 6,
        "MIN_INIT_BATTERY": 60,
        "MAX_INIT_BATTERY": 100,
        "MIN_OPERABLE_BATTERY": 2,
        "MAX_RANGE": 5,
        "BATTERY_TOLLS": {
            'COMMUNICATION': 5e-4,
            'MOVEMENT': 6e-4,
            'ALREADY_VISITED': 2.5e-4,
        },
        "TIME_TOLLS": {
            'SCAN': 1e-3,
            'TIMEOUT': 1e-3,
            'PER_RANGE': 0.5e-3,
            'LEFTOVER': 1e-3,
            'ALREADY_VISITED': 1e-3,
            'LEADER_TO_LEADER': 1e-3
        },

        "LEADERS_COORDINATES": [(0, 0), (0, 3), (3, 0), (3, 3)]
    }

    annots = params["ROWS"] <= 30 and params["COLS"] <= 30
    run_experiment("original_radar", params, annotations=annots)


# def scenario0():
#     params = {
#         "ROWS": 2,
#         "COLS": 2,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario0", params, annotations=annots)

# def scenario1():
#     params = {
#         "ROWS": 3,
#         "COLS": 3,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario1", params, annotations=annots)

# def scenario2():
#     params = {
#         "ROWS": 4,
#         "COLS": 4,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario2", params, annotations=annots)

# def scenario3():
#     params = {
#         "ROWS": 5,
#         "COLS": 5,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0),(4, 4)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario3", params, annotations=annots)

# def scenario4():
#     params = {
#         "ROWS": 7,
#         "COLS": 7,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0),(0, 6),(3, 3)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario4", params, annotations=annots)

# def scenario5():
#     params = {
#         "ROWS": 10,
#         "COLS": 10,
#         "MIN_INIT_BATTERY": 60,
#         "MAX_INIT_BATTERY": 100,
#         "MIN_OPERABLE_BATTERY": 2,
#         "MAX_RANGE": 5,
#         "BATTERY_TOLLS": {
#             'COMMUNICATION': 5e-4,
#             'MOVEMENT': 6e-4,
#             'ALREADY_VISITED': 2.5e-4,
#         },
#         "TIME_TOLLS": {
#             'SCAN': 2e-3,
#             'TIMEOUT': 1e-3,
#             'PER_RANGE': 0.5e-3,
#             'LEFTOVER': 3e-3,
#             'ALREADY_VISITED': 1e-3,
#             'LEADER_TO_LEADER': 1e-3
#         },

#         "LEADERS_COORDINATES": [(0, 0),(0, 9),(5, 5),(9, 0),(9, 9)]
#     }

#     annots = params["ROWS"] <= 30 and params["COLS"] <= 30
#     run_experiment("scenario5", params, annotations=annots)


def cdta_runner():
    for leaders_num in [1, 2, 4, 8, 16, 32, 64]:
        for rows_cols in [2, 4, 8, 16, 32, 64]:

            if leaders_num >= math.isqrt(rows_cols**2):
                continue

            leaders_coordinates = []
            leaders_domain = []

            subgrid_size = rows_cols // math.isqrt(leaders_num)

            for i in range(leaders_num):
                leader_row = (i // math.isqrt(leaders_num)) * subgrid_size
                leader_col = (i % math.isqrt(leaders_num)) * subgrid_size

                leader_row = min(leader_row, rows_cols - subgrid_size)
                leader_col = min(leader_col, rows_cols - subgrid_size)

                leaders_coordinates.append((leader_row, leader_col))
                leaders_domain.append(
                    [(leader_row, leader_col), (leader_row + subgrid_size - 1, leader_col + subgrid_size - 1)])

            print(leaders_coordinates, leaders_domain)
            params = {
                "ROWS": rows_cols,
                "COLS": rows_cols,
                "MIN_INIT_BATTERY": 60,
                "MAX_INIT_BATTERY": 100,
                "MIN_OPERABLE_BATTERY": 2,
                "MAX_RANGE": -1,
                "BATTERY_TOLLS": {
                    'COMMUNICATION': 5e-4,
                },
                "TIME_TOLLS": {
                    'COMMUNICATION': 1e-3,
                    'LEADER_TO_LEADER': 1e-3
                },
                "LEADERS_COORDINATES": leaders_coordinates,
                "LEADERS_DOMAIN": leaders_domain
            }

            run_cdta('cdta_{leaders_num}_{population}'.format(leaders_num=leaders_num,
                     population=params['ROWS'] * params['COLS']), params)


def starring_runner():
    for leaders_num in [1, 2, 4, 8, 16, 32, 64]:
        for rows_cols in [2, 4, 8, 16, 32, 64]:

            if leaders_num >= math.isqrt(rows_cols**2):
                continue

            leaders_coordinates = []
            leaders_domain = []

            subgrid_size = rows_cols // math.isqrt(leaders_num)

            for i in range(leaders_num):
                leader_row = (i // math.isqrt(leaders_num)) * subgrid_size
                leader_col = (i % math.isqrt(leaders_num)) * subgrid_size

                leader_row = min(leader_row, rows_cols - subgrid_size)
                leader_col = min(leader_col, rows_cols - subgrid_size)

                leaders_coordinates.append((leader_row, leader_col))
                leaders_domain.append(
                    [(leader_row, leader_col), (leader_row + subgrid_size - 1, leader_col + subgrid_size - 1)])

            print(leaders_coordinates, leaders_domain)
            params = {
                "ROWS": rows_cols,
                "COLS": rows_cols,
                "MIN_INIT_BATTERY": 60,
                "MAX_INIT_BATTERY": 100,
                "MIN_OPERABLE_BATTERY": 2,
                "MAX_RANGE": -1,
                "BATTERY_TOLLS": {
                    'COMMUNICATION': 5e-4,
                },
                "TIME_TOLLS": {
                    'COMMUNICATION': 1e-3,
                    'LEADER_TO_LEADER': 1e-3
                },
                "LEADERS_COORDINATES": leaders_coordinates,
                "LEADERS_DOMAIN": leaders_domain
            }

            run_experiment_simplified_star('sr_{leaders_num}_{population}'.format(leaders_num=leaders_num,
                                                                                  population=params['ROWS'] * params['COLS']), params)


def dring_runner():
    for leaders_num in [1, 2, 4, 8, 16, 32, 64]:
        for rows_cols in [2, 4, 8, 16, 32, 64]:

            if leaders_num >= math.isqrt(rows_cols**2):
                continue

            leaders_coordinates = []
            leaders_domain = []

            subgrid_size = rows_cols // math.isqrt(leaders_num)

            for i in range(leaders_num):
                leader_row = (i // math.isqrt(leaders_num)) * subgrid_size
                leader_col = (i % math.isqrt(leaders_num)) * subgrid_size

                leader_row = min(leader_row, rows_cols - subgrid_size)
                leader_col = min(leader_col, rows_cols - subgrid_size)

                leaders_coordinates.append((leader_row, leader_col))
                leaders_domain.append(
                    [(leader_row, leader_col), (leader_row + subgrid_size - 1, leader_col + subgrid_size - 1)])

            print(leaders_coordinates, leaders_domain)
            params = {
                "ROWS": rows_cols,
                "COLS": rows_cols,
                "MIN_INIT_BATTERY": 60,
                "MAX_INIT_BATTERY": 100,
                "MIN_OPERABLE_BATTERY": 2,
                "MAX_RANGE": -1,
                "BATTERY_TOLLS": {
                    'COMMUNICATION': 5e-4,
                },
                "TIME_TOLLS": {
                    'COMMUNICATION': 1e-3,
                    'LEADER_TO_LEADER': 1e-3
                },
                "LEADERS_COORDINATES": leaders_coordinates,
                "LEADERS_DOMAIN": leaders_domain
            }

            run_experiment_simplified_ring('dr_{leaders_num}_{population}'.format(leaders_num=leaders_num,
                                                                                  population=params['ROWS'] * params['COLS']), params)

# scenario0()
# scenario1()
# scenario2()
# scenario3()
# scenario4()
# scenario5()
# cdta()
# our_star_approach()
# our_ring_approach()
# original_radar()


# cdta_runner()
# starring_runner()
dring_runner()
