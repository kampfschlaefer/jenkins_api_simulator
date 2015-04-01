
from flask import Flask, request, make_response
import pprint

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True


@app.route('/api/python', methods=['GET'])
def handle_api_python():
    logger.debug('Requested /api/python')
    ret = {'jobs': []}
    return pprint.pformat(ret)
