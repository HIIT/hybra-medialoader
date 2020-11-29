# -*- coding: utf-8 -*-

## XXX fixeme

import sys
sys.path.insert(0, '../sites/')

import requests
import collections
import processor
from datetime import datetime
import pickle
import json
import os

def make_request( base_url, app_id, app_key, limit = 1000, offset = 0):

    api_request = ( base_url + '/articles.json?' +
    '&orderby=published desc' +
    '&limit=' + str( limit ) + '&offset=' + str( offset ) +
    '&app_id=' + app_id + '&app_key=' + app_key +
    '&fields=publisher,url,subjects,datePublished,dateContentModified,headline,lead,authors,content' )

    request = requests.get( api_request )

    if request.status_code >= 400:
        print(request.status_code)
        print(request.text)

    return request

def parse(news_items):

    news = news_items.json()[ 'data' ]

    list_to_return = []

    for data in news:

        ## Might be smarter to just specify the relevant stuff in the request

        ## What should this contain?
        publisher = data.get( 'publisher', {} ).get( 'name', u'' )

        url = data.get( 'url', {} ).get( 'full', u'' )

        ## News obtained via Articles API have tons of categories
        ## Let's grab them all for now

        categories = [ x.get('title', {} ).get( 'fi', u'' ) for x in data.get( 'subjects', [ {} ] ) ]

        ## Note: this loses information about the timezone

        datetime_list = [ data.get( 'datePublished', u'' ), data.get( 'dateContentModified', u'' ) ]
        datetime_list = list( map( processor.strip_datetime_object, datetime_list ) )

        title = data.get( 'headline' ).get( 'full', u'' )
        ingress = data.get( 'lead', u'' )

        ## This only gets the name of the first author

        author = data.get( 'authors', u'' )
        if author != u'':
            author = author[0].get( 'name', u'' )

        text = filter( lambda x: x.get( 'type' ) == 'text', data.get( 'content' ) )
        text = [ t[ 'text' ] for t in text ]
        text = ' '.join( text )

        ## Articles API only gives Yle Images API ids, not urls

        images = filter( lambda x: x.get( 'type' ) == 'image', data.get( 'content' ) )
        image_ids = [ image.get( 'id', u'' ) for image in images ]
        image_urls = [ 'http://images.cdn.yle.fi/image/upload//' + image_id +
                      '.jpg' for image_id in image_ids ]
        image_captions = [ image.get( 'alt', u'' ) for image in images ]

        dictionary_item = processor.create_dictionary( publisher, url, news_items.status_code,
                                           categories, datetime_list, author,
                                           title, ingress, text, image_urls, image_captions )

        list_to_return.append( dictionary_item )

    return list_to_return

def resort_pickles( raw_dir ):

    store = collections.defaultdict( list )

    for d in os.listdir( raw_dir ):

        data = pickle.load( open( raw_dir + d , "rb") )

        time_format = '%Y-%m-%d %H:%M:%S'

        if int( data['http'] ) == 200:

            try:

                #domain = re.match( __urlpat , data['url'] ).group('domain')

                domain = data[ 'domain' ]

                datetimes = data[ 'datetime_list' ]
                datetime_list = []

                for date_time in datetimes:
                    date_time = datetime.strptime(date_time, time_format)
                    datetime_list.append(date_time)

                #datetime.strptime( news_item.get('datetime_list')[0], time_format)

                time = max( datetime_list )

                destination = 'yle_' + domain + '_' + str( time.year ) + '_' + str( time.month )
                data['datetime_list'] = list (map( str, data['datetime_list'] ) ) ## transform dateties to string

                store[ destination ].append( data ) ## TODO: potentially just directly write to file, if we run out of memory

            except Exception as e: ## sometimes not all data things are there, and thus let's prepeare for it
                print(e)

    return store

def api_download( base_url, app_id, app_secret, max_iterations = 1000, item_limit = 1000, raw_dir = 'data-raw/' ):

    ## Just in case things don't yet work as expexted,
    ## this will by default run for 1000 rounds
    ## Set to 0 when calling to get _everything_
    max_iterations = max_iterations

    ## Specify how many items will be returned with each call
    item_limit = item_limit

    i = 0

    old_month_items = []

    while True:

        news_items = make_request( base_url, app_id, app_secret, limit = item_limit, offset = i * item_limit )

        news_items = parse( news_items )
        j = 0

        for news_item in news_items:

            with open( raw_dir + str(i) + '_' + str(j) + '.pickle', 'wb' ) as f:
                pickle.dump(news_item, f)

                j = j + 1

        i = i + 1

        print(str(i) + ' out of ' + str(max_iterations))

        ## Break if max number of iterations has been reached
        ## or if the response from the API contains fewer elements than the limit
        if (max_iterations > 0 and i == max_iterations) or (len(news_items) < item_limit):
            break



if __name__ == '__main__':

    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--key', default='yle_keys.json' )
        parser.add_argument('--iteration', default = 10)
        args = parser.parse_args()
        keys = json.load( open( args.key ), strict = False )
    except:
        print('Can not read keys')
        quit()

    raw_dir = 'data-raw/' ## where pickles are stored
    data_dir = 'data/' ## where json outputs are stored

    ## Downloads 10 pages of 1000 items each
    ## and dumps each news item in a pickle

    api_download( keys['url'], keys['app_id'], keys['app_key'], max_iterations = int( args.iteration ), item_limit = 1000, raw_dir = raw_dir )

    ## Combines pickles and dumps them in
    ## 'yle_domain_year_month' json files

    store = resort_pickles( raw_dir )

    for filename, data in store.items():

        json.dump( data , open( data_dir + filename + '.json', 'w' ), indent = 2)
