
from flask import Flask, request, make_response
import requests

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

jenkins_url = 'http://localhost:8000'


@app.route('/api/python', methods=['GET'])
def handle_forward():
    logger.info('Request for /api/python')
    logger.info(
        'path %s, method %s, data "%s"',
        request.path, request.method, request.data
    )
    if request.method == 'GET':
        r = requests.get('%s%s' % (jenkins_url, request.path))
        logger.info(
            'got reponse from jenkins:\n  status_code = %s\n'
            '  headers =\n%s\n  text =\n%s' % (
                r.status_code, r.headers, r.text
            )
        )
        headers = {}
        for h in ['content-type', 'x-jenkins-session', 'x-jenkins', 'server']:
            headers[h] = r.headers[h]
        response = make_response((r.text, r.status_code, headers))
        return response

    return '{}'
