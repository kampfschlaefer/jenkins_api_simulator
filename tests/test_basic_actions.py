
import logging
from jenkinsapi import jenkins
import pytest
from pytest_localserver.http import WSGIServer

from jenkins_api_simulator import passthrough
from jenkins_api_simulator import statefull
passthrough.jenkins_url = 'http://localhost:8080'


def pytest_generate_tests(metafunc):
    if 'app' in metafunc.fixturenames:
        apps = [statefull.app]
        ids = ['statefull']
        if metafunc.config.option.jenkins:
            apps.append(passthrough.app)
            ids.append('passthrough')
        metafunc.parametrize('app', apps, ids=ids)


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


@pytest.yield_fixture
def single_job_jenkins(myjenkins):
    myjenkins.create_job('test_job_01', open('tests/basic_job.xml', 'r').read())
    yield myjenkins
    myjenkins.delete_job('test_job_01')


def test_get_first_job(single_job_jenkins):
    jobname = single_job_jenkins.keys()[0]
    assert jobname

    first_job = single_job_jenkins[jobname]
    assert first_job is not None
    assert first_job.name == jobname


def test_run_job(single_job_jenkins):
    job = single_job_jenkins.get_job('test_job_01')

    qi = job.invoke()
    assert qi.queue_id
