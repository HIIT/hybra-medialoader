# -*- coding: utf-8 -*-

import requests
import collections
import processor
from datetime import datetime
import pickle
import json

def dump( data ):

    ## Get month
    date = data[0].get( 'datetime_list' )
    date = date[0][0:7]
    date = date.replace( '-', '_' )

    month = date[5:7]
    if month[0] == '0':
        date = date[0:5] + date[6:7]

    ## Get 'domain' (e.g 'Yle Uutiset', 'Yle Novosti', 'svenska-nyheter')
    ## and for each domain dump data in a file named 'yle_domain_year_month.json'

    domain_set = set( [ d.get( 'domain' ) for d in data ] )

    for domain in domain_set:
        domain_data = filter( lambda x: x.get( 'domain' ) == domain, data )
        domain = domain.replace( ' ', '_' )

        print 'Dumping ' + 'yle_' + domain + '_' + date + '.json'

        f = open( 'yle_' + domain + '_' + date + '.json', 'w' )
        json.dump( domain_data, f )
        f.close()

        f = open( 'yle_' + domain + '_' + date + '.pickle', 'w' )
        pickle.dump( domain_data, f )
        f.close()

def separate_months( news_items, old_month_items ):

    news_items = old_month_items + news_items

    time_format = '%Y-%m-%d %H:%M:%S'

    datetimes = [ datetime.strptime( news_item.get('datetime_list')[0], time_format) for news_item in news_items ]

    ## Get months in format yyyy-m

    months = set( [ str( date.year ) + '-' + str( date.month ) for date in datetimes ] )

    months_dict = collections.defaultdict(list)

    for news_item in news_items:

        news_item_date = datetime.strptime( news_item.get('datetime_list')[0], time_format )
        news_item_month = str( news_item_date.year ) + '-' + str( news_item_date.month )

        months_dict[news_item_month].append(news_item)

    month_keys = sorted( months_dict, key = lambda x: datetime.strptime( x, '%Y-%m' ), reverse = True )

    ## If dict has only one month's data,
    ## this month is still incomplete, so return it

    if len( months_dict ) == 1:
        return months_dict[ months_dict.keys()[0] ]

    ## Otherwise dump finished months

    for month in month_keys:

        if month == months_dict.keys()[ len(months_dict) - 1 ]:
            return months_dict[ month ]

        dump( months_dict[ month ] )

def make_request( limit, offset ):

    # Currently uses API's test environment

    app_id = ''
    app_key = ''

    base_url = 'https://articles.api-test.yle.fi/v2/articles.json?'

    api_request = ( base_url +
    '&orderby=published desc' +
    '&limit=' + str( limit ) + '&offset=' + str( offset ) +
    '&app_id=' + app_id + '&app_key=' + app_key +
    '&fields=publisher,url,subjects,datePublished,dateContentModified,headline,lead,authors,content' )

    request = requests.get( api_request )

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
        datetime_list = map( processor.strip_datetime_object, datetime_list )

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

def api_download( max_iterations = 1000, item_limit = 1000 ):

    ## Just in case things don't yet work as expexted,
    ## this will by default run for 1000 rounds
    ## Set to 0 when calling to get _everything_
    max_iterations = max_iterations

    ## Specify how many items will be returned with each call
    item_limit = item_limit

    i = 0

    old_month_items = []

    while True:

        print i

        news_items = make_request( limit = item_limit, offset = i * item_limit )
        news_items = parse( news_items )
        month_data = separate_months( news_items, old_month_items )
        old_month_items = month_data

        i = i + 1

        if ( len( news_items ) < item_limit ) or ( max_iterations > 0 and i == max_iterations ):
            dump( old_month_items )
            break

if __name__ == '__main__':
    ## Downloads 10 pages of 1000 items each and dumps them
    api_download( max_iterations = 10, item_limit = 1000 )
