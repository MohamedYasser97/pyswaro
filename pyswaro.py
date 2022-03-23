from sre_constants import FAILURE
import numpy as np
import random

ROWS, COLS = (8, 8)
MIN_INIT_BATTERY = 50
MAX_INIT_BATTERY = 100
BATTERY_TOLLS = {
  'COMMUNICATION': 0.05
}
TIME_TOLLS = {
  'SCAN': 4e-3,
  'TIMEOUT': 2,
  'PER_RANGE': 1e-3
}

LEADERS_COORDINATES = [(2,0), (2,5), (5,5), (7,1)]
terrain = [[]]
visited = [[]]
total_time_consumed = 0


def init_terrain():
  global terrain, visited
  terrain = [[0] * COLS] * ROWS
  visited = [[0] * COLS] * ROWS


def init_charge_batteries():
  global terrain
  terrain = np.random.randint(MIN_INIT_BATTERY, MAX_INIT_BATTERY + 1, size=(ROWS, COLS))
  terrain = terrain.tolist()


def set_leaders():
  global terrain
  for i, j in LEADERS_COORDINATES:
    terrain[i][j] = 100


def check_visited():
  for i in range(0,ROWS):
    for j in range(0,COLS):
      if visited[i][j] == 0:
        return False
  return True


def drain_battery(i, j, toll_type = 'COMMUNICATION'):
  global terrain
  terrain[i][j] -= BATTERY_TOLLS[toll_type]

def leader_scan(scan_range):
  global terrain, visited, total_time_consumed
  for i, j in LEADERS_COORDINATES:
    failures = 0

    # Scan right
    if j+scan_range < COLS:
      if visited[i][j+scan_range]==0:
        visited[i][j+scan_range] = 1

      drain_battery(i, j) # Leader
      drain_battery(i, j+scan_range) # Subordinate
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else: # If there's no subordinate then it's a wasted comm from leader
      failures += 1

    # Scan left
    if j-scan_range >= 0:
      if visited[i][j-scan_range]==0:
        visited[i][j-scan_range] = 1

      drain_battery(i, j)
      drain_battery(i, j-scan_range)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan up
    if i-scan_range >= 0:
      if visited[i-scan_range][j]==0:
        visited[i-scan_range][j] = 1

      drain_battery(i, j)
      drain_battery(i-scan_range, j)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan down
    if i+scan_range < ROWS:
      if visited[i+scan_range][j]==0:
        visited[i+scan_range][j] = 1

      drain_battery(i, j)
      drain_battery(i+scan_range, j)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan NE
    if i-scan_range >= 0 and j+scan_range < COLS:
      if visited[i-scan_range][j+scan_range]==0:
        visited[i-scan_range][j+scan_range] = 1

      drain_battery(i, j)
      drain_battery(i-scan_range, j+scan_range)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan NW
    if i-scan_range >= 0 and j-scan_range >= 0:
      if visited[i-scan_range][j-scan_range]==0:
        visited[i-scan_range][j-scan_range] = 1

      drain_battery(i, j)
      drain_battery(i-scan_range, j-scan_range)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan SE
    if i+scan_range < ROWS and j+scan_range < COLS:
      if visited[i+scan_range][j+scan_range]==0:
        visited[i+scan_range][j+scan_range] = 1

      drain_battery(i, j)
      drain_battery(i+scan_range, j+scan_range)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1

    # Scan SW
    if i+scan_range < ROWS and j-scan_range >= 0:
      if visited[i+scan_range][j-scan_range]==0:
        visited[i+scan_range][j-scan_range] = 1

      drain_battery(i, j)
      drain_battery(i+scan_range, j-scan_range)
      total_time_consumed += 2 * (TIME_TOLLS['SCAN'] + TIME_TOLLS['PER_RANGE'] * scan_range)
    else:
      failures += 1
    
    # Calculate failure tolls for leader
    for i in range(failures):
      drain_battery(i, j)
      total_time_consumed += TIME_TOLLS['SCAN'] + (TIME_TOLLS['PER_RANGE'] * scan_range)
      total_time_consumed += TIME_TOLLS['TIMEOUT'] + (TIME_TOLLS['PER_RANGE'] * scan_range)


init_terrain()
init_charge_batteries()
set_leaders()
