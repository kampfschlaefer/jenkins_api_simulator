
from flask import Flask, request, make_response
import requests

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

jenkins_url = 'http://localhost:8000'


def prepare_response(response):
    _headers = {}
    for h in ['content-type', 'x-jenkins-session', 'x-jenkins', 'server']:
        _headers[h] = response.headers[h]
    _content = response.text.replace(jenkins_url, request.url_root.strip('/'))
    return make_response((_content, response.status_code, _headers))


@app.route('/api/python', methods=['GET'])
def handle_api_python():
    logger.info('Request for /api/python')
    logger.info(
        'path %s, method %s, data "%s"',
        request.path, request.method, request.data
    )
    if request.method == 'GET':
        r = requests.get('%s%s' % (jenkins_url, request.path))
        return prepare_response(r)
        # content = r.text.replace(jenkins_url, request.url_root.strip('/'))
        # logger.info(
        #     'got reponse from jenkins:\n  status_code = %s\n'
        #     '  headers =\n%s\n  text =\n%s' % (
        #         r.status_code, r.headers, content
        #     )
        # )
        # headers = {}
        # for h in ['content-type', 'x-jenkins-session', 'x-jenkins', 'server']:
        #     headers[h] = r.headers[h]
        # response = make_response((content, r.status_code, headers))
        # return response

    return '{}'


@app.route('/job/<name>/api/python', methods=['GET'])
def handle_job(name):
    logger.info('Requesting job %s', name)
    r = requests.get('%s%s' % (jenkins_url, request.path))
    return prepare_response(r)
