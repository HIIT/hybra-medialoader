# -*- coding: utf-8 -*-

import requests
import collections
import processor
from datetime import datetime
import pickle
import json

def dump(data, file_name):

    f = open(file_name + '.json', 'w')
    json.dump(data, f)
    f.close()

    f = open(file_name + '.pickle', 'w')
    pickle.dump(data, f)
    f.close()

def paging(api_request, max_iterations = 0):

    ## Set max iterations to 0 if you want _everything_
    max_iterations = max_iterations

    ## Specify how many items will be returned with each call
    item_limit = 1000

    i = 0

    while True:

        news_items = parse(api_request = '', limit = item_limit, offset = i * item_limit)

        dump(news_items, str(i))

        if (len(news_items) < item_limit) or (max_iterations > 0 and i == max_iterations) :
            break

        i = i + 1

def make_request(api_request, limit, offset):

    # Currently uses API's test environment

    app_id = ''
    app_key = ''

    base_url = 'https://articles.api-test.yle.fi/v2/articles.json?'

    api_request = base_url + api_request + '&limit=' + str(limit) + '&offset=' + str(offset) + '&app_id=' + app_id + '&app_key=' + app_key

    r = requests.get( api_request )

    return r

def parse(api_request, limit, offset):

    r = make_request(api_request, limit, offset)

    news = r.json()['data']

    list_to_return = []

    for data in news:

        publisher = data.get('publisher', u'')
        url = data.get('url', {}).get('full', u'')

        ## News obtained via Articles API have tons of categories
        ## Let's grab them all

        categories = [x.get('title', {}).get('fi', u'') for x in data.get('subjects', [{}])]
        datetime_list = [data.get('datePublished', u''), data.get('dateContentModified', u'')]
        title = data.get('headline').get('full', u'')
        ingress = data.get('lead', u'')

        ## This only gets the name of the first author

        author = data.get('authors', u'')
        if author is not u'':
            author = author[0].get('name', u'')

        text = filter(lambda x: x.get('type') == 'text', data.get('content'))
        text = [t['text'] for t in text]
        text = ' '.join(text)

        ## Articles API only gives Yle Images API ids, not urls

        images = filter(lambda x: x.get('type') == 'image', data.get('content'))
        image_ids = [image.get('id', u'') for image in images]
        image_captions = [image.get('alt', u'') for image in images]

        dictionary_item = processor.create_dictionary(u'', url, r.status_code,
                                           categories, datetime_list, author,
                                           title, ingress, text, image_ids, image_captions)

        list_to_return.append(dictionary_item)

    return list_to_return

if __name__ == '__main__':
    ## Downloads 10 pages of 1000 items each and dumps them
    paging('', 10)
