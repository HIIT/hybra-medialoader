import sys
import os
import re

## store data
import json
import pickle

urlpat = r'((http[s]?):\/\/)?(\w+\.)*(?P<domain>\w+)\.(\w+)(\/.*)?'

error = open( 'error.log', 'w' )

data_dir = 'data/'

if not os.path.exists( data_dir ):
    os.makedirs( data_dir )

def download( id, url, storeto ):

    url = url.strip()


    try:
        ## try to dynamically load the correct script using the domain name
        loader = re.match( urlpat , url ).group('domain')

        loader = __import__( 'sites.' + loader, fromlist = [ loader ] )

        story = loader.parse( url )

        if 'json' in storeto:
            json.dump( story , open( data_dir + str(id) + '.json', 'w' ) )

        if 'pickle' in storeto:
            pickle.dump( story , open( data_dir + str(id) + '.pickle', 'w' ) )

        return story['http']

    except Exception, e:
        print e
        print "Failed " + url

        error.write( url + '\n' )



if __name__ == '__main__':

    import collections

    http_status = collections.defaultdict( int )

    for f in sys.argv[1:]:

        f = open( f )
        for id, url in enumerate( f ):

            s = download( id, url, 'pickle' )

            http_status[ s ] += 1

    print 'Final status'
    for s, c in http_status.items():
        print s, '\t', c
