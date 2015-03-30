
import logging
from jenkinsapi import jenkins
import pytest
from pytest_localserver.http import WSGIServer

from jenkins_api_simulator import passthrough


@pytest.yield_fixture(scope='module')
def passthrough_server():
    _server = WSGIServer(application=passthrough.app)
    _server.start()
    yield _server
    _server.stop()


def test_get_jobs(passthrough_server):
    passthrough.jenkins_url = 'http://localhost:8080'

    j = jenkins.Jenkins(passthrough_server.url)
    logging.info(j.keys())
    assert j.keys()
