
import logging
from jenkinsapi import jenkins
import pytest
from pytest_localserver.http import WSGIServer

from jenkins_api_simulator import passthrough
passthrough.jenkins_url = 'http://localhost:8080'


@pytest.yield_fixture(scope='module')
def passthrough_server():
    _server = WSGIServer(application=passthrough.app)
    _server.start()
    yield _server
    _server.stop()


@pytest.fixture
def myjenkins(passthrough_server):
    return jenkins.Jenkins(passthrough_server.url)


def test_get_jobs(myjenkins):
    logging.info(myjenkins.keys())
    assert myjenkins.keys()


def test_get_first_job(myjenkins):
    jobname = myjenkins.keys()[0]
    assert jobname

    first_job = myjenkins[jobname]
    assert first_job is not None
    assert first_job.name == jobname
