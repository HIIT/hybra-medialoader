import sys
import os

path = os.path.abspath('.')
sys.path.append(path)

import downloader as d

good_urls = [
    'http://yle.fi/uutiset/tv-uutisten_politiikantoimittaja_timo_kuparinen_kuollut/9167149',
    'http://www.hs.fi/kotimaa/art-2000005007566.html',
    'http://www.iltasanomat.fi/musiikki/art-2000005008209.html'
]
bad_urls = ['http://example.com', 'http://www.example.org']


class TestParser:

    @classmethod
    def setup_class(self):

        self.raw_path = 'test-data-raw/'
        self.data_path = 'test-data/'
        self.errors = 'test-errors.log'

        errors = open( self.errors, 'w')

        for f in [ self.raw_path, self.data_path ]:
            if not os.path.exists( f ):
                os.makedirs( f )

        for url in good_urls:
            d.download( url , self.raw_path, errors )

        for url in bad_urls:
            d.download( url , self.raw_path, errors )

        self.collected = d.resort_pickles( self.raw_path )

    def test_downloaded_files_exists(self):
        assert len( os.listdir( self.raw_path ) ) == len( good_urls )

    def test_errors_logged(self):
        assert len( open( self.errors ).readlines() ) == len( bad_urls )

    def test_file_contents_ok(self):

        import pickle

        keys = ['url', 'http', 'categories', 'datetime_list', 'author', 'title', 'ingress', 'text', 'images', 'captions']

        for d in os.listdir( self.raw_path ):
            d = pickle.load( open( self.raw_path + d ) )
            for key in keys:
                assert key in d

    def test_pickles_sorted_correctly(self):
        count = sum( map( lambda x: len( x ), self.collected.values() ) )
        assert count == len( good_urls )

    def test_pickles_sorted_keys(self):

        ## check file names
        assert 'yle' in ''.join( self.collected.keys() )
        assert 'hs' in ''.join( self.collected.keys() )
        assert 'iltasanomat' in ''.join( self.collected.keys() )

        ## years
        assert '2016' in ''.join( self.collected.keys() )

        ## month
        assert '9' in ''.join( self.collected.keys() )
        assert '12' in ''.join( self.collected.keys() )
