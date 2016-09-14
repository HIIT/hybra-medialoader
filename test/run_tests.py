import sys
import os
import importlib
import pytest

path = os.path.abspath('..')
sys.path.append(path)

out = 'test_file.txt'
url_list = 'test_urls.txt'

def run_parser_tests():
    urls = open(url_list, 'r')

    for url in urls:
        domain = get_domain(url)
        module = importlib.import_module('sites.' + domain)
        initialise_file(module, url)
        pytest.main() # Pitäisi keksiä miten testeille annetaan argumentteja

    urls.close()

def get_domain(url):
    protocol,domain,path = url.split(".")
    if (domain == 'blogit'): # The special case of Iltalehti blogs
        domain = 'blogit_iltalehti'
    return domain

def initialise_file(module, url):
    if ( os.path.isfile(out) ):
        os.remove(out)
    module.parse(url, file(out, 'w'))

if __name__ == '__main__':
    run_parser_tests()
