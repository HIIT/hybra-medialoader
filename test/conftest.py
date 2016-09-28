def pytest_addoption(parser):
    parser.addoption("--domain", action="append", default=[],
        help="list of stringinputs to pass to test functions")
    parser.addoption("--url", action="append", default=[],
        help="list of stringinputs to pass to test functions")

def pytest_generate_tests(metafunc):
    if 'domain' in metafunc.fixturenames:
        metafunc.parametrize("domain",
                             metafunc.config.option.domain)
    if 'url' in metafunc.fixturenames:
        metafunc.parametrize("url",
                             metafunc.config.option.url)
