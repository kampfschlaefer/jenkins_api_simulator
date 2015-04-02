
def pytest_addoption(parser):
    parser.addoption(
        '--jenkins', action='store', default=None,
        help='url of local jenkins to run passthrough-tests against'
    )
