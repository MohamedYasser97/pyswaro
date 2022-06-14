import json
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

vars = {}
with open('vars.json', 'r') as openfile:
    vars = json.load(openfile)

ROWS, COLS = (vars["ROWS"], vars["COLS"])
MIN_INIT_BATTERY = vars["MIN_INIT_BATTERY"]
MAX_INIT_BATTERY = vars["MAX_INIT_BATTERY"]
MIN_OPERABLE_BATTERY = vars["MIN_OPERABLE_BATTERY"]
MAX_RANGE = vars["MAX_RANGE"]
BATTERY_TOLLS = vars["BATTERY_TOLLS"]
TIME_TOLLS = vars["TIME_TOLLS"]

LEADERS_COORDINATES = vars["LEADERS_COORDINATES"]

terrain = [[]]
visited = [[]]
leader_tally = []
leftovers = 0
total_time_consumed = 0


def init():
    global terrain, visited, leader_tally
    terrain = np.random.randint(
        MIN_INIT_BATTERY, MAX_INIT_BATTERY + 1, size=(ROWS, COLS))
    visited = np.zeros([ROWS, COLS])
    leader_tally = np.zeros(len(LEADERS_COORDINATES))


def set_leaders():
    global terrain
    for i, j in LEADERS_COORDINATES:
        terrain[i][j] = 100


def check_visited():
    global visited
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if visited[i][j] == 0 and (i, j) not in LEADERS_COORDINATES:
                return False
    return True


def drain_battery(i, j, toll_type='COMMUNICATION'):
    global terrain
    terrain[i][j] -= BATTERY_TOLLS[toll_type]


def leader_scan(scan_range, finished_leaders):
    global terrain, visited, total_time_consumed
    current_leader = 0
    for i, j in LEADERS_COORDINATES:
        if (i, j) in finished_leaders or terrain[i][j] <= MIN_OPERABLE_BATTERY:
            continue

        failures = 0
        cur_visited_nodes = 0

        # Scan right
        if j+scan_range < COLS and terrain[i][j+scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i][j+scan_range] == 0:
                visited[i][j+scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)  # Leader
                drain_battery(i, j+scan_range)  # Subordinate
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')  # Leader
                # Subordinate
                drain_battery(i, j+scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:  # If there's no subordinate then it's a wasted comm from leader
            failures += 1

        # Scan left
        if j-scan_range >= 0 and terrain[i][j-scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i][j-scan_range] == 0:
                visited[i][j-scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i, j-scan_range)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i, j-scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan up
        if i-scan_range >= 0 and terrain[i-scan_range][j] >= MIN_OPERABLE_BATTERY:
            if visited[i-scan_range][j] == 0:
                visited[i-scan_range][j] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i-scan_range, j)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i-scan_range, j, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan down
        if i+scan_range < ROWS and terrain[i+scan_range][j] >= MIN_OPERABLE_BATTERY:
            if visited[i+scan_range][j] == 0:
                visited[i+scan_range][j] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i+scan_range, j)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i+scan_range, j, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan NE
        if i-scan_range >= 0 and j+scan_range < COLS and terrain[i-scan_range][j+scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i-scan_range][j+scan_range] == 0:
                visited[i-scan_range][j+scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i-scan_range, j+scan_range)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i-scan_range, j+scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan NW
        if i-scan_range >= 0 and j-scan_range >= 0 and terrain[i-scan_range][j-scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i-scan_range][j-scan_range] == 0:
                visited[i-scan_range][j-scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i-scan_range, j-scan_range)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i-scan_range, j-scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan SE
        if i+scan_range < ROWS and j+scan_range < COLS and terrain[i+scan_range][j+scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i+scan_range][j+scan_range] == 0:
                visited[i+scan_range][j+scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i+scan_range, j+scan_range)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i+scan_range, j+scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Scan SW
        if i+scan_range < ROWS and j-scan_range >= 0 and terrain[i+scan_range][j-scan_range] >= MIN_OPERABLE_BATTERY:
            if visited[i+scan_range][j-scan_range] == 0:
                visited[i+scan_range][j-scan_range] = 1
                leader_tally[current_leader] += 1
                drain_battery(i, j)
                drain_battery(i+scan_range, j-scan_range)
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                cur_visited_nodes += 1
                drain_battery(i, j, 'ALREADY_VISITED')
                drain_battery(i+scan_range, j-scan_range, 'ALREADY_VISITED')
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)
        else:
            failures += 1

        # Calculate failure tolls for leader
        for failure in range(failures):
            drain_battery(i, j)
            total_time_consumed += TIME_TOLLS['SCAN'] + \
                (TIME_TOLLS['PER_RANGE'] * scan_range)
            total_time_consumed += TIME_TOLLS['TIMEOUT'] + \
                (TIME_TOLLS['PER_RANGE'] * scan_range)

        if failures > 4 or cur_visited_nodes > 4:
            finished_leaders.append((i, j))

        current_leader += 1

    return finished_leaders


def scan_leftovers():
    global visited, total_time_consumed, leftovers
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if visited[i][j] == 0 and terrain[i][j] >= MIN_OPERABLE_BATTERY:
                visited[i][j] = 1
                leftovers += 1

    for i, j in LEADERS_COORDINATES:
        for k in range(int(((leftovers/(ROWS*COLS))*100)/len(LEADERS_COORDINATES))):
            drain_battery(i, j, 'MOVEMENT')

        total_time_consumed += TIME_TOLLS['LEFTOVER'] + \
            ((leftovers/(ROWS*COLS))/len(LEADERS_COORDINATES))


def leader_count():
    scan_range = 1
    finished_leaders = []
    while check_visited() == False:
        if scan_range == MAX_RANGE:
            scan_leftovers()
            break
        finished_leaders = leader_scan(scan_range, finished_leaders)
        scan_range += 1


# Maybe add timeouts in the future
def leaders_meeting():
    global total_time_consumed
    for i, j in LEADERS_COORDINATES:
        terrain[i][j] -= BATTERY_TOLLS['COMMUNICATION'] * \
            (len(LEADERS_COORDINATES)-1)

    total_time_consumed += TIME_TOLLS['LEADER_TO_LEADER'] * \
        len(LEADERS_COORDINATES)


# Same as leader_count() but to inform them of total number.
# Subordinates know what to do based on the total number.
def leaders_subordinates_meeting():
    global visited, leader_tally, leftovers

    leftovers = 0
    visited = np.zeros([ROWS, COLS])
    leader_tally = np.zeros(len(LEADERS_COORDINATES))
    leader_count()


def draw_terrain(terrain, annotations=True, subtitle='Operation Results', save=True):
    figure, axes = plt.subplots(1, 2, sharex=False, figsize=(ROWS, COLS))

    figure.suptitle(subtitle)
    axes[0].set_title('Terrain Battery Levels')
    axes[1].set_title('Battery Levels Histogram')

    hmap = sns.heatmap(ax=axes[0], data=terrain, annot=annotations, cmap='Greens',
                       cbar=False, fmt='d', xticklabels=False, yticklabels=False)

    for i, j in LEADERS_COORDINATES:
        hmap.add_patch(
            Rectangle((i, j), 1, 1, fill=False, edgecolor='gold', lw=3))

    sns.histplot(data=terrain.flatten(), kde=True)

    if save == True:
        figure = plt.gcf()
        figure.set_size_inches(17, 9)
        plt.savefig('plot')
    else:
        plt.show()


def log(data):
    with open('log.txt', 'a+') as openfile:
        pprint(data, stream=openfile)


def common_routine(save_plot=True):
    init()
    set_leaders()

    log('Initial terrain:')
    log(terrain)

    leader_count()

    log('Leader count:')
    log(terrain)

    log('Visited:')
    log(visited)

    log('Counted:')
    log(np.sum(leader_tally) + leftovers)

    leaders_meeting()

    log('Leaders meeting: ')
    log(terrain)

    leaders_subordinates_meeting()

    log('Leaders to subs: ')
    log(terrain)

    log('Visited: ')
    log(visited)

    log('Operable nodes: ')
    log(np.sum(leader_tally) + leftovers)

    draw_terrain(terrain, save_plot)
    log(f'Total time consumed: {total_time_consumed} seconds')
    # TODO: handle simultaneous actions with respect to consumed time
