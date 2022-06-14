import json
import os
import tarfile

from pyswaro import common_routine, draw_terrain, log

config = {}
with open('vars.json', 'r') as openfile:
    config = json.load(openfile)


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


def run_experiment(experiment_name):
    create_dir_and_visit(experiment_name)
    log(config)
    common_routine()
    go_back()


def experiment_xyz():
    params = {
        "ROWS": 5,
        "COLS": 5,
        "MIN_INIT_BATTERY": 50,
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

        "LEADERS_COORDINATES": [(0, 0), (0, 4), (4, 0), (4, 4), (2, 2)]
    }

    change_params(params)
    run_experiment("xyz")


experiment_xyz()
