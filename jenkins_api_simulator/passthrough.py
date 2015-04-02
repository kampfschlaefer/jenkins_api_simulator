
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
        try:
            _headers[h] = response.headers[h]
        except KeyError:
            pass
    try:
        _headers['location'] = response.headers['location'].replace(
            jenkins_url,
            request.url_root.strip('/')
        )
    except KeyError:
        pass
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
        # print(' Will return %s' % r.text)
        return prepare_response(r)

    return '{}'


@app.route('/job/<name>/api/python', methods=['GET'])
def handle_job(name):
    logger.info('Requesting job %s', name)
    r = requests.get('%s%s' % (jenkins_url, request.path))
    logger.info('Answer is %s', r.text)
    return prepare_response(r)


@app.route('/job/<name>/doDelete', methods=['POST'])
def post_delete_job(name):
    logger.info('Deleting job %s', name)
    r = requests.post('%s%s' % (jenkins_url, request.path))
    logger.info('Response is %i: %s', r.status_code, r.text)
    return prepare_response(r)


@app.route('/job/<name>/build', methods=['POST'])
def post_build_job(name):
    logger.info('Building job %s', name)
    r = requests.post('%s%s' % (jenkins_url, request.path))
    logger.info('Response is %i: %s', r.status_code, r.text)
    return prepare_response(r)


@app.route('/job/<name>/config.xml', methods=['GET'])
def get_job_config(name):
    logger.info('Getting job %s config.xml', name)
    r = requests.get('%s%s' % (jenkins_url, request.path))
    logger.info('Response is %i: %s', r.status_code, r.text)
    return prepare_response(r)


@app.route('/createItem', methods=['POST'])
def post_create_job():
    logger.info('Posting new job \'%s\'', request.args['name'])
    logger.info(' Request data is %s', request.data)
    r = requests.post(
        '%s%s' % (jenkins_url, request.path),
        params=request.args,
        data=request.data,
        headers={'Content-Type': 'application/xml'}
    )
    logger.info('Answer is %s', r.text)
    return prepare_response(r)


@app.route('/queue/item/<number>/api/python', methods=['GET'])
def get_queue_item(number):
    logger.info('Getting queue item %s', number)
    r = requests.get('%s%s' % (jenkins_url, request.path))
    logger.info(' Answer is %i: %s', r.status_code, r.text)
    return prepare_response(r)
