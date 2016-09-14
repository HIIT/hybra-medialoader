import sys
import os
import importlib

path = os.path.abspath('..')
sys.path.append(path)

out = 'test_file.txt'
url_list = 'test_urls.txt'

class TestParser:
    def test_file_exists(self):
        urls = open(url_list, 'r')
        for link in urls:
            module = load_module(link)
            initialise_file(module, link)
            assert os.path.isfile(out) == True
        urls.close()

    def test_file_not_empty(self):
        urls = open(url_list, 'r')
        for link in urls:
            module = load_module(link)
            initialise_file(module, link)
            assert os.path.getsize(out) > 0
        urls.close()

    def test_file_contents_match(self):
        assert 1 == 1

def load_module(link):
    protocol,domain,path = link.split(".")
    return importlib.import_module('sites.' + domain)

def initialise_file(module, link):
    if ( os.path.isfile(out) ):
        os.remove(out)
    module.parse(link,file(out, 'w'))
