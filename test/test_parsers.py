import sys
import os
import importlib
import filecmp

path = os.path.abspath('..')
sys.path.append(path)

out = 'test_file.txt'
url_list = 'urls.txt'

class TestParser:
    def test_file_exists(self):
        urls = open(url_list, 'r')
        for url in urls:
            domain = get_domain(url)
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url)
            assert os.path.isfile(out) == True
        urls.close()

    def test_file_not_empty(self):
        urls = open(url_list, 'r')
        for url in urls:
            domain = get_domain(url)
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url)
            assert os.path.getsize(out) > 0
        urls.close()

    def test_file_contents_match(self):
        urls = open(url_list, 'r')
        for url in urls:
            domain = get_domain(url)
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url)
            assert filecmp.cmp(out, 'test_contents/' + domain + '.txt')
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
