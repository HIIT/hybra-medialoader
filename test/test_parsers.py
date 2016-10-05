import sys
import os
import filecmp
import difflib
import importlib
import datetime

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
        write_difference_log( domain, test_content_path )
        assert filecmp.cmp( test_content_path, out )

    def test_dictionary_created(self, domain, url):
        module = importlib.import_module('sites.' + domain)
        assert bool( module.parse(url) )

    def test_dictionary_contains_right_keys(self, domain, url):
        module = importlib.import_module('sites.' + domain)
        d = module.parse( url )
        keys = ['url', 'http', 'categories', 'datetime_list', 'author', 'title', 'ingress', 'text', 'images', 'captions']
        for key in keys:
            assert key in d

    def test_dictionary_values_correct_type(self, domain, url):
        module = importlib.import_module('sites.' + domain)
        d = module.parse( url )

        assert type( d['url'] ) is str
        assert type( d['http'] ) is str

        assert type( d['categories'] ) is list
        for category in d['categories']:
            type( category ) is str

        assert type( d['datetime_list'] ) is list
        for datetime_object in d['datetime_list']:
            assert type( datetime_object ) is datetime.datetime

        assert type( d['author'] ) is str
        assert type( d['title'] ) is str
        assert type( d['ingress'] ) is str
        assert type( d['text'] ) is str

        assert type( d['images'] ) is list
        for img in d['images']:
            assert type( img ) is str

        assert type( d['captions'] ) is list
        for caption in d['captions']:
            assert type( caption ) is str


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
