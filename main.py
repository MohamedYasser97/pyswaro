import json
import os

from pyswaro import common_routine


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
    common_routine(annots=annotations)
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


experiment_xyz()
