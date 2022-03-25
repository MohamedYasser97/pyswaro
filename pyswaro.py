from pprint import pprint
import numpy as np

ROWS, COLS = (7, 7)
MIN_INIT_BATTERY = 50
MAX_INIT_BATTERY = 100
MAX_RANGE = 5
BATTERY_TOLLS = {
    'COMMUNICATION': 0.05,
    'MOVEMENT': 0.5
}
TIME_TOLLS = {
    'SCAN': 2e-3,
    'TIMEOUT': 3e-3,
    'PER_RANGE': 0.5e-3,
    'LEFTOVER': 3e-3,
    'ALREADY_VISITED': 1e-3
}

LEADERS_COORDINATES = [(3, 3)]
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


def leader_scan(scan_range):
    global terrain, visited, total_time_consumed
    current_leader = 0
    for i, j in LEADERS_COORDINATES:
        failures = 0

        # Scan right
        if j+scan_range < COLS:
            if visited[i][j+scan_range] == 0:
                visited[i][j+scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)  # Leader
            drain_battery(i, j+scan_range)  # Subordinate
        else:  # If there's no subordinate then it's a wasted comm from leader
            failures += 1

        # Scan left
        if j-scan_range >= 0:
            if visited[i][j-scan_range] == 0:
                visited[i][j-scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i, j-scan_range)
        else:
            failures += 1

        # Scan up
        if i-scan_range >= 0:
            if visited[i-scan_range][j] == 0:
                visited[i-scan_range][j] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i-scan_range, j)
        else:
            failures += 1

        # Scan down
        if i+scan_range < ROWS:
            if visited[i+scan_range][j] == 0:
                visited[i+scan_range][j] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i+scan_range, j)
        else:
            failures += 1

        # Scan NE
        if i-scan_range >= 0 and j+scan_range < COLS:
            if visited[i-scan_range][j+scan_range] == 0:
                visited[i-scan_range][j+scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i-scan_range, j+scan_range)
        else:
            failures += 1

        # Scan NW
        if i-scan_range >= 0 and j-scan_range >= 0:
            if visited[i-scan_range][j-scan_range] == 0:
                visited[i-scan_range][j-scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i-scan_range, j-scan_range)
        else:
            failures += 1

        # Scan SE
        if i+scan_range < ROWS and j+scan_range < COLS:
            if visited[i+scan_range][j+scan_range] == 0:
                visited[i+scan_range][j+scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i+scan_range, j+scan_range)
        else:
            failures += 1

        # Scan SW
        if i+scan_range < ROWS and j-scan_range >= 0:
            if visited[i+scan_range][j-scan_range] == 0:
                visited[i+scan_range][j-scan_range] = 1
                leader_tally[current_leader] += 1
                total_time_consumed += 2 * \
                    (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
            else:
                total_time_consumed += 2 * \
                    (TIME_TOLLS['ALREADY_VISITED'] +
                     TIME_TOLLS['PER_RANGE'] * scan_range)

            drain_battery(i, j)
            drain_battery(i+scan_range, j-scan_range)
        else:
            failures += 1

        # Calculate failure tolls for leader
        for failure in range(failures):
            drain_battery(i, j)
            total_time_consumed += TIME_TOLLS['SCAN'] + \
                (TIME_TOLLS['PER_RANGE'] * scan_range)
            total_time_consumed += TIME_TOLLS['TIMEOUT'] + \
                (TIME_TOLLS['PER_RANGE'] * scan_range)

        current_leader += 1


def scan_leftovers():
    global visited, total_time_consumed, leftovers
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if visited[i][j] == 0:
                visited[i][j] = 1
                leftovers += 1

    for i, j in LEADERS_COORDINATES:
        drain_battery(i, j, 'MOVEMENT')
        total_time_consumed += TIME_TOLLS['LEFTOVER']


def leader_count():
    scan_range = 1
    while check_visited() == False:
        if scan_range == MAX_RANGE:
            scan_leftovers()
            break
        leader_scan(scan_range)
        scan_range += 1


init()
set_leaders()

pprint('Terrain before:')
pprint(terrain)

leader_count()

pprint('Terrain after:')
pprint(terrain)

pprint('Visited after:')
pprint(visited)

pprint('Counted:')
pprint(np.sum(leader_tally) + leftovers)

pprint(f'Total time consumed: {total_time_consumed} seconds')
# TODO: Deal with idle time and depleted batteries
