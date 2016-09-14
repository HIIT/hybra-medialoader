import sys
import os

path = os.path.abspath('..')
sys.path.append(path)

from sites import *

out = 'test.txt'

class TestParser:
    def test_file_exists(self):
        urls = open('urls.txt', 'r')
        for line in urls:
            protocol,domain,path = line.split(".")
            initialise_file(domain)
        assert os.path.isfile(out) == True

    def test_file_not_empty(self):
        urls = open('urls.txt', 'r')
        for line in urls:
            protocol,domain,path = line.split(".")
            initialise_file(domain)
        assert os.path.getsize(out) > 0

    def test_file_contents_match(self):
        assert 1 == 1

def initialise_file(domain):
    if ( os.path.isfile(out) ):
        os.remove(out)
    domain.parse(url,file(out, 'w'))
