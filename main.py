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


def run(experiment_name):
    create_dir_and_visit(experiment_name)
    log(config)
    common_routine()
    go_back()


def experiment_xyz():
    # configure json params here
    run()
