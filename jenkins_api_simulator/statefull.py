
from flask import Flask, request, make_response, url_for
import pprint

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

jobs = {}


@app.route('/')
def index():
    return 'Simulated Jenkins Index'


@app.route('/job/<jobname>', methods=['GET'])
def get_job(jobname):
    return ''


@app.route('/job/<jobname>/api/python', methods=['GET'])
def get_job_api(jobname):
    jobinfo = {
        "actions":[],
        "description":"",
        "displayName":jobname,
        "displayNameOrNull":None,
        "name":jobname,
        "url":url_for('get_job', jobname=jobname, _external=True),
        "buildable":True,
        "builds":[],
        "color":"notbuilt",
        "firstBuild":None,
        "healthReport":[],
        "inQueue":False,
        "keepDependencies":False,
        "lastBuild":None,
        "lastCompletedBuild":None,
        "lastFailedBuild":None,
        "lastStableBuild":None,
        "lastSuccessfulBuild":None,
        "lastUnstableBuild":None,
        "lastUnsuccessfulBuild":None,
        "nextBuildNumber":1,
        "property":[],
        "queueItem":None,
        "concurrentBuild":False,
        "downstreamProjects":[],
        "scm":{},
        "upstreamProjects":[]
    }
    logger.debug('will return %s', pprint.pformat(jobinfo))
    return pprint.pformat(jobinfo)


@app.route('/job/<jobname>/doDelete', methods=['POST'])
def post_job_delete(jobname):
    if jobname in jobs:
        del jobs[jobname]
        return 'job %s deleted' % jobname
    else:
        raise Exception('Job %s not found' % jobname)


@app.route('/api/python', methods=['GET'])
def handle_api_python():
    logger.debug('Requested /api/python')
    ret = {
        'assignedLabels': [{}],
        'mode': 'NORMAL',
        'nodeDescription': 'Simulated Jenkins',
        'nodeName': '',
        'numExecutors': 0,
        'description': '',
        'overallLoad': {},
        'primaryView': {'name': 'Alle', 'url': url_for('index', _external=True)},
        'quietingDown': False,
        'slaveAgentPort': 0,
        'unlabeledLoad': {},
        'useCrumbs': False,
        'useSecurity': False,
        'views': [{'name': 'Alle', 'url': url_for('index', _external=True)}],
        'jobs': [{
            'name': k,
            'color': 'notbuilt',
            'url': url_for('get_job', jobname=k, _external=True)
        } for k in jobs]
    }
    logger.debug(' Will return %s', ret)
    return pprint.pformat(ret)

@app.route('/createItem', methods=['POST'])
def post_create_item():
    name = request.args['name']
    config = request.data
    jobs[name] = {'config': config}
    return ''
