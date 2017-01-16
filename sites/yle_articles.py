# -*- coding: utf-8 -*-

import requests
import collections
import processor
from datetime import datetime
import pickle
import json

def dump(data):

    ## Get month
    date = data[0].get('datetime_list')[0][0:7]
    date = date.replace('-', '_')

    ## Get 'domain' (e.g 'Yle Uutiset', 'Yle Novosti', 'svenska-nyheter')
    ## and for each domain dump data in a file named 'domain_year_month.json'

    domain_set = set([d.get('domain') for d in data])

    for domain in domain_set:
        domain_data = filter(lambda x: x.get('domain') == domain, data)
        domain = domain.replace(' ', '_')

        print 'Dumping ' + domain + '_' + date + '.json'

        f = open(domain + '_' + date + '.json', 'w')
        json.dump(domain_data, f)
        f.close()

        f = open(domain + '_' + date + '.pickle', 'w')
        pickle.dump(domain_data, f)
        f.close()

def separate_months(news_items, old_month_items):

        ## Loop through the downloaded news items and check the month of each
        ## If month changes, dump previous files and move the rest of the news
        ## to the next month
        ##
        ## Quite ugly as it is

        last_date = ''

        if len(old_month_items) == 0:
            last_date = datetime.strptime(news_items[0].get('datetime_list')[0], '%Y-%m-%d %H:%M:%S')
        else:
            last_date = datetime.strptime(news_items[0].get('datetime_list')[0], '%Y-%m-%d %H:%M:%S')

        changed_month = False

        for news_item in news_items:
            current_date = datetime.strptime(news_item.get('datetime_list')[0], '%Y-%m-%d %H:%M:%S')

            if current_date.month != last_date.month:

                new_month_items = (filter(lambda x: datetime.strptime(x.get('datetime_list')[0], '%Y-%m-%d %H:%M:%S').month == current_date.month, news_items))
                old_month_items = old_month_items + filter(lambda x: datetime.strptime(x.get('datetime_list')[0], '%Y-%m-%d %H:%M:%S').month == last_date.month, news_items)

                dump(old_month_items)

                old_month_items = new_month_items
                new_month_items = []
                changed_month = True

                break

        if not changed_month:
            new_month_items = news_items
            old_month_items = old_month_items + new_month_items

        return (old_month_items, new_month_items)

def api_download(max_iterations = 1000):

    ## Just in case things don't yet work as expexted
    ## Set to 0 when calling to get _everything_
    max_iterations = max_iterations

    ## Specify how many items will be returned with each call
    item_limit = 1000

    i = 0

    new_month_items = []
    old_month_items = []

    while True:

        print i

        news_items = make_request(limit = item_limit, offset = i * item_limit)

        news_items = parse(news_items)

        month_data = separate_months(news_items, old_month_items)

        old_month_items = month_data[0]
        new_month_items = month_data[1]

        if (len(news_items) < item_limit) or (max_iterations > 0 and i == max_iterations):
            dump(old_month_items)
            break

        i = i + 1

def make_request(limit, offset):

    # Currently uses API's test environment

    app_id = ''
    app_key = ''

    base_url = 'https://articles.api-test.yle.fi/v2/articles.json?'

    api_request = (base_url +
    '&orderby=published desc' +
    '&limit=' + str(limit) + '&offset=' + str(offset) +
    '&app_id=' + app_id + '&app_key=' + app_key)

    r = requests.get( api_request )

    return r

def parse(news_items):

    news = news_items.json()['data']

    list_to_return = []

    for data in news:

        ## Might be smarter to just specify the relevant stuff in the request

        ## What should this contain?
        publisher = data.get('publisher', {}).get('name', u'')

        url = data.get('url', {}).get('full', u'')

        ## News obtained via Articles API have tons of categories
        ## Let's grab them all

        categories = [x.get('title', {}).get('fi', u'') for x in data.get('subjects', [{}])]

        ## Note: this loses information about the timezone

        datetime_list = [data.get('datePublished', u''), data.get('dateContentModified', u'')]
        datetime_list = map(processor.strip_datetime_object, datetime_list)

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

        dictionary_item = processor.create_dictionary(publisher, url, news_items.status_code,
                                           categories, datetime_list, author,
                                           title, ingress, text, image_ids, image_captions)

        list_to_return.append(dictionary_item)

    return list_to_return

if __name__ == '__main__':
    ## Downloads 10 pages of 1000 items each and dumps them
    api_download(10)
