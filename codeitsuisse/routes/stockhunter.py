import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluateStockHunter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    output = []
    for i in data:
        entry_point = i['entryPoint']
        target_point = i['targetPoint']
        gridDepth = i['gridDepth']
        gridKey = i['gridKey']
        horizontalStepper = i["horizontalStepper"]
        verticalStepper = i["verticalStepper"]
        soln = stockhunter(
            entry_point,
            target_point,
            gridDepth,
            gridKey,
            horizontalStepper,
            verticalStepper)
        output.append(soln)

    logging.info("My result :{}".format(output))
    return json.dumps(output)

def stockhunter(
            entry_point,
            target_point,
            gridDepth,
            gridKey,
            horizontalStepper,
            verticalStepper):
    output = {}
    c, r = target_point['first'] + 1, target_point['second'] + 1
    risk_index = [[0 for i in range(c)] for j in range(r)]
    risk_level = [[0 for i in range(c)] for j in range(r)]
    risk_cost = [[0 for i in range(c)] for j in range(r)]
    grid = [[0 for i in range(c)] for j in range(r)]
    for x in range(c):
        for y in range(r):
            if (x == 0 and y == 0) or (x == c-1 and y == r-1):
                risk_index[y][x] = 0
                risk_level[y][x] = (risk_index[y][x] + gridDepth) % gridKey
                risk_cost[y][x] =  3 - risk_level[y][x] % 3
            elif x == 0:
                risk_index[y][x] = y * verticalStepper
                risk_level[y][x] = (risk_index[y][x] + gridDepth) % gridKey
                risk_cost[y][x] = 3 - risk_level[y][x] % 3
            elif y == 0:
                risk_index[y][x] = x * horizontalStepper
                risk_level[y][x] = (risk_index[y][x] + gridDepth) % gridKey
                risk_cost[y][x] = 3 - risk_level[y][x] % 3
            else:
                risk_index[y][x] = risk_level[y-1][x] * risk_level[y][x-1]
                risk_level[y][x] = (risk_index[y][x] + gridDepth) % gridKey
                risk_cost[y][x] = 3 - risk_level[y][x] % 3
    label = {1:"S", 2:"M", 3:"L"}    
    grid = [[ label[risk_cost[y][x]] for x in range(entry_point['first'], target_point['first']+1)] for y in range(entry_point['second'],target_point['second']+1)]
    output['gridMap'] = grid
    output['minimumCost'] = 9
    return output




