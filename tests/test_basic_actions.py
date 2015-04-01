
import logging
from jenkinsapi import jenkins
import pytest
from pytest_localserver.http import WSGIServer

from jenkins_api_simulator import passthrough
from jenkins_api_simulator import statefull
passthrough.jenkins_url = 'http://localhost:8080'


def pytest_generate_tests(metafunc):
    if 'app' in metafunc.fixturenames:
        metafunc.parametrize(
            'app',
            (passthrough.app,statefull.app),
            ids=['passthrough', 'statefull']
        )


@pytest.yield_fixture
def jenkins_server(app):
    _server = WSGIServer(application=app)
    _server.start()
    yield _server
    _server.stop()


@pytest.fixture
def myjenkins(jenkins_server):
    return jenkins.Jenkins(jenkins_server.url)


def test_get_jobs(myjenkins):
    logging.info(myjenkins.keys())
    assert isinstance(myjenkins.keys(), list)


def test_create_test_job(myjenkins):
    myjenkins.create_job('test_job_01', open('tests/basic_job.xml', 'r').read())

    assert myjenkins.keys()
    assert 'test_job_01' in myjenkins.keys()

    myjenkins.delete_job('test_job_01')


def test_get_first_job(myjenkins):
    jobname = myjenkins.keys()[0]
    assert jobname

    first_job = myjenkins[jobname]
    assert first_job is not None
    assert first_job.name == jobname
