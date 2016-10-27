import sys
import os
import filecmp
import importlib
import datetime
import common

path = os.path.abspath('.')
sys.path.append(path)

domain = 'iltalehti'
url = 'http://www.iltalehti.fi/ulkomaat/2016101322454951_ul.shtml'

out = 'test/parser_out.txt'
module = importlib.import_module( 'sites.' + domain )
d = module.parse(url)

class TestParser:

    @classmethod
    def setup_class(cls):
        common.initialise_file( out, d )

    def test_file_exists(self):
        assert os.path.isfile(out)

    def test_file_not_empty(self):
        assert os.path.getsize(out) > 0

    def test_file_contents_match(self):
        test_content_path = 'test/test_contents/' + domain + '.txt'
        common.write_difference_log( domain, out, test_content_path )
        assert filecmp.cmp( test_content_path, out )

    def test_dictionary_created(self):
        assert bool( d )

    def test_dictionary_contains_right_keys(self):
        keys = ['url', 'http', 'categories', 'datetime_list', 'author', 'title', 'ingress', 'text', 'images', 'captions']
        for key in keys:
            assert key in d

    def test_dictionary_values_correct_type(self):
        assert type( d['url'] ) is str
        assert type( d['http'] ) is str

        assert type( d['categories'] ) is list
        for category in d['categories']:
            type( category ) is str

        assert type( d['datetime_list'] ) is list
        for datetime_object in d['datetime_list']:
            assert type( datetime_object ) is datetime.datetime or datetime.date

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
