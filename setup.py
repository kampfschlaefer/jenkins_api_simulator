
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            #'-x',
            '-v',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='jenkins_api_simulator',
    version='0.1',
    author='Arnold Krille',
    author_email='arnold@arnoldarts.de',
    packages=find_packages(),
    install_requires=[
        'requests==2.6.0',
        'flask==0.10.1',
        'gevent==1.0.1',
    ],
    tests_require=[
        'pytest>=2.6.0',
        'pytest-localserver>=0.3.4',
        'pytest-capturelog>=0.7',
        'jenkinsapi>=0.2.26'
    ],
    cmdclass={
        'test': PyTest,
    }
)
