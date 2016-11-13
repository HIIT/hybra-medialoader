import sys
import os
import re

## store data
import json

urlpat = r'((http[s]?):\/\/)?(\w+\.)*(?P<domain>\w+)\.(\w+)(\/.*)?'

error = open( 'error.log', 'w' )

def download( id, url, storeto ):

    url = url.strip()


    try:
        ## try to dynamically load the correct script using the domain name
        loader = re.match( urlpat , url ).group('domain')

        loader = __import__( 'sites.' + loader, fromlist = [ loader ] )

        story = loader.parse( url )

        if 'json' in storeto:
            json.dump( story , open( 'data/' + str(id) + '.json', 'w' ) )

    except Exception, e:
        print e
        print "Failed " + url

        error.write( url + '\n' )



if __name__ == '__main__':

    for f in sys.argv[1:]:

        f = open( f )
        for id, url in enumerate( f ):

            download( id, url, 'json' )
