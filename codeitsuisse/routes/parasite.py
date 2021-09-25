import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    output = []
    for testcase in data:
        testcase_output = parasite(testcase)
        output.append(testcase_output)

    
    
    logging.info("My result :{}".format(output))
    return json.dumps(output)




def parasite(info):
    results = {
        "room": info['room'],
        "p1": {indiv:-1 for indiv in info['interestedIndividuals']},
        "p2": 0,
        "p3": 0,
        "p4": 0
    }
    grid_status_p1 = [x[:] for x in info['grid']]
    r,c = len(grid_status_p1), len(grid_status_p1[0])
    indiv_coord = []
    for indiv in info['interestedIndividuals']:
        coords = tuple(map(int, indiv.split(",")))
        if grid_status_p1[coords[0]][coords[1]] == 0:
            results['p1'][indiv] = -1
        elif grid_status_p1[coords[0]][coords[1]] == 1:
            no_one_around = all([grid_status_p1[n[0]][n[1]] == 0 for n in find_neighbors(coords,grid_status_p1)])
            if no_one_around:
                results['p1'][indiv] = -1
                continue
            else:
                indiv_coord.append(coords)
        elif grid_status_p1[coords[0]][coords[1]] == 2:
            results['p1'][indiv] = -1
        elif grid_status_p1[coords[0]][coords[1]] == 3:
            results['p1'][indiv] = 0
    
    time = 0
    current_state_p1 = [x[:] for x in grid_status_p1]
    prev_grid_status_p1 = [x[:] for x in grid_status_p1]
    while True:
        print(current_state_p1)
        time +=1 
        for i in range(r):
            for j in range(c):
                if prev_grid_status_p1[i][j] == 1:
                    nn = find_neighbors((i,j),grid_status_p1) 
                    infected_nearby = any([prev_grid_status_p1[n[0]][n[1]] == 3 for n in nn])
                    if infected_nearby:
                        current_state_p1[i][j] = 3
                        if (i,j) in indiv_coord:
                            results['p1'][str(i)+","+str(j)] = time
        if prev_grid_status_p1 == current_state_p1:
            break
        prev_grid_status_p1 = [x[:] for x in current_state_p1]    
    healthy_remains = any([prev_grid_status_p1[i][j] == 1 for j in range(c) for i in range(r)])
    if healthy_remains:
        results['p2'] = -1
    else:
        results['p2'] = time  
    return results

def find_neighbors(coords,grid):
    r,c = len(grid), len(grid[0])
    directions = [[0,1], [1,0], [-1,0], [0,-1]]
    neighbors = []
    for d in directions:
        if  (0<=coords[0]+d[0]) and (coords[0]+d[0]<r) and (0<=coords[1]+d[1]) and (coords[1]+d[1]<c):
            neighbors.append((coords[0]+d[0],coords[1]+d[1]))
    return neighbors

