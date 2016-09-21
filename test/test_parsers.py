import sys
import os
import filecmp
import difflib

path = os.path.abspath('..')
sys.path.append(path)

out = 'parser_out.txt'

class TestParser:

    def test_file_exists(self):
        assert os.path.isfile(out)

    def test_file_not_empty(self):
        assert os.path.getsize(out) > 0

    def test_file_contents_match(self, domain):
        test_content_path = 'test_contents/' + domain + '.txt'
        write_difference_log(domain, test_content_path)
        assert filecmp.cmp(test_content_path, out)


def write_difference_log(domain, test_content_path):
    diff_log = file('difference_logs/' + domain + '_diff.txt', 'w')

    test_content = open(test_content_path, 'r')
    content = open(out, 'r')

    test_content_text = test_content.read().replace(' ', ' \n')
    content_text = content.read().replace(' ', ' \n')

    test_content_lines = test_content_text.splitlines()
    content_lines = content_text.splitlines()

    d = difflib.Differ()
    diff = d.compare(test_content_lines, content_lines)
    diff_log.write( '\n'.join(diff) )

    test_content.close()
    content.close()
