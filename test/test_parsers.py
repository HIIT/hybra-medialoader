import sys
import os
import filecmp

path = os.path.abspath('..')
sys.path.append(path)

out = 'test_file.txt'

class TestParser:

    def test_file_exists(self):
        assert os.path.isfile(out)

    def test_file_not_empty(self):
        assert os.path.getsize(out) > 0

    def test_file_contents_match(self, domain):
        assert filecmp.cmp(out, 'test_contents/' + domain + ".txt")
