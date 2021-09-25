import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['GET'])
def evaluateTTT():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    



