# -*- coding: utf-8 -*-

import requests
import collections
import processor
from datetime import datetime
import pickle
import json

def parse(api_request):

    # Currently uses API's test environment

    app_id = ''
    app_key = ''

    base_url = 'https://articles.api-test.yle.fi/v2/articles.json?'

    api_request = base_url + api_request + '&app_id=' + app_id + '&app_key=' + app_key

    r = requests.get( api_request )

    news = r.json()['data']

    list_to_return = []

    for data in news:

        publisher = data.get('publisher', u'')
        url = data.get('url', {}).get('full', u'')

        ## News obtained via Articles API have tons of categories
        categories = [x.get('title', {}).get('fi', u'') for x in data.get('subjects', [{}])]

        datetime_list = [data.get('datePublished', u''), data.get('dateContentModified', u'')]
        title = data.get('headline').get('full', u'')
        ingress = data.get('lead', u'')

        author = data.get('authors', u'')
        if author is not u'':
            author = author[0].get('name', u'')

        text = filter(lambda x: x.get('type') == 'text', data.get('content'))
        text = [t['text'] for t in text]
        text = ' '.join(text)

        # API only gives image ids, not urls

        images = filter(lambda x: x.get('type') == 'image', data.get('content'))
        image_ids = [image['id'] for image in images]
        image_captions = [image['alt'] for image in images]

        dictionary_item = processor.create_dictionary(u'', url, r.status_code,
                                           categories, datetime_list, author,
                                           title, ingress, text, image_ids, image_captions)

        list_to_return.append(dictionary_item)

    return list_to_return

if __name__ == '__main__':
    parse('published_after=2016-12-20T12:00:00%2b0300&offset=0&limit=10&orderby=published desc')
