import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for rock in data.get("test_cases"):
        output = {}
        origin, score = best_shot(rock)
        output['input'] = rock
        output['score'] = score
        output['origin'] = origin
        results.append(output)
    logging.info("My result :{}".format(results))
    return json.dumps(results)


def best_shot(rock):
    valid_index = []
    current = rock[0]
    for i in range(1,len(rock)):
        if current != rock[i]:
            valid_index.append(i-1)
            current = rock[i]
    valid_index.append(i)
    valid_index.insert(0,0)
    valid_origin = []
    for i in range(1, len(valid_index)):
        valid_origin.append((valid_index[i]+valid_index[i-1])//2)

    best_score = 0
    best_origin = 0
    
    for origin in valid_origin: 
        current = rock[origin]  
        left_index = origin - 1
        right_index = origin + 1
        prev_left, prev_right = -1, -1
        score = 0
        while True:
            while left_index >= 0:
                if rock[left_index] != current:
                    break
                left_index -= 1
            while right_index < len(rock):
                if rock[right_index] != current:
                    break
                right_index += 1
            if left_index <0 and right_index >= len(rock):
                score += score_multiplied((len(rock) - prev_right) + (prev_left + 1))
                break
            if left_index <0:
                score += score_multiplied(right_index)
                break
            if right_index >= len(rock):
                score += score_multiplied(len(rock) - left_index)
                break
            if rock[left_index] != rock[right_index]:
                score += score_multiplied((right_index - prev_right) + (prev_left - left_index) - 1)
                break
            else:
                current = rock[left_index]
                if prev_left == -1 and prev_right == -1:
                    score += score_multiplied(right_index - left_index - 1)
                    prev_left, prev_right = left_index, right_index
                else:
                    score += score_multiplied((right_index - prev_right) + (prev_left - left_index))
                    prev_left, prev_right = left_index, right_index
        if score > best_score:
            best_origin = origin
            best_score = score
    return best_origin, best_score

def score_multiplied(score):
    if score >= 10:
        return score*2
    elif score >=7: 
        return score*1.5
    else:
        return score
