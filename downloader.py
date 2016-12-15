import sys
import os
import re

## store data
import json
import pickle

import base64

import collections

__urlpat = r'((http[s]?):\/\/)?(\w+\.)*(?P<domain>\w+)\.(\w+)(\/.*)?'


def download( url, raw_dir, error ):

    url = url.strip()


    try:
        ## try to dynamically load the correct script using the domain name
        loader = re.match( __urlpat , url ).group('domain')

        loader = __import__( 'sites.' + loader, fromlist = [ loader ] )

        story = loader.parse( url )

        f = base64.encodestring( url )

        pickle.dump( story , open( raw_dir + f + '.pickle', 'w' ) )

        return story['http']

    except Exception, e:
        print e
        print "Failed " + url

        error.write( url + '\n' )


def resort_pickles( raw_dir ):

    store = collections.defaultdict( list )

    for d in os.listdir( raw_dir ):

        data = pickle.load( open( raw_dir + d ) )

        if int( data['http'] ) == 200:

            try:

                domain = re.match( __urlpat , data['url'] ).group('domain')

                time = max( data['datetime_list'] )

                destination = domain + '_' + str( time.year ) + '_' + str( time.month )
                data['datetime_list'] = map( str, data['datetime_list'] ) ## transform dateties to string

                store[ destination ].append( data ) ## TODO: potentially just directly write to file, if we run out of memory

            except Exception, e:
                print e

    return store

if __name__ == '__main__':

    raw_dir = 'data-raw/' ## where pickles are stored
    data_dir = 'data/' ## where json outputs are stored

    for f in [raw_dir, data_dir]:

        if not os.path.exists( f ):
            os.makedirs( f )

    http_status = collections.defaultdict( int )

    for f in sys.argv[1:]:

        error = open( 'error_' + f + '.log', 'w' )

        f = open( f )
        for id, url in enumerate( f ):

            s = download( url, raw_dir, error )

            http_status[ s ] += 1

    print 'Final status'
    for s, c in http_status.items():
        print s, '\t', c

    ## regroup files to nicer folders
    store = resort_pickles( raw_dir )

    ## store files as json
    for filename, data in store.items():
        json.dump( data , open(  data_dir + filename + '.json', 'w' ) )
