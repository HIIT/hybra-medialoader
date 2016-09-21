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
        for line in urls:
            domain,url = line.split(",")
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url.strip())
            if (os.path.isfile(out) == False):
                print domain + " -> file does not exist"
            assert os.path.isfile(out)
        urls.close()

    def test_file_not_empty(self):
        urls = open(url_list, 'r')
        for line in urls:
            domain,url = line.split(",")
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url.strip())
            if (os.path.getsize(out) == 0):
                print domain + " -> file is empty"
            assert os.path.getsize(out) > 0
        urls.close()

    def test_file_contents_match(self):
        urls = open(url_list, 'r')
        for line in urls:
            domain,url = line.split(",")
            module = importlib.import_module('sites.' + domain)
            initialise_file(module, url.strip())
            assert filecmp.cmp(out, 'test_contents/' + domain + ".txt")
        urls.close()

def initialise_file(module, url):
    if ( os.path.isfile(out) ):
        os.remove(out)
    module.parse(url, file(out, 'w'))
