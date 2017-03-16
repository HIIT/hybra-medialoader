# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime


def parse_from_archive(url, content):

    article = BeautifulSoup( content, "html.parser" )

    if article == None:
        return processor.create_dictionary('Pohjolan sanomat', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

    meta = article.find( class_ = 'hakutuloslahde' )

    datetime_list = processor.collect_datetime( meta )

    categories = [processor.collect_text( meta ).split(',')[1].strip()]

    author = processor.collect_text( article.find( class_ = 'signeeraus' ) )

    title = processor.collect_text( article.find( class_ = 'otsikko' ) )

    ingress = processor.collect_text( article.find_all( class_ = 'jalkirivi')[1] )
    ingress += ' ' + processor.collect_text( article.find( class_ = 'esirivi' ) )
    ingress = ingress.strip()

    text_divs = article.find_all( class_ = 'artikkelip')
    text = ''
    for text_content in text_divs:
        text += processor.collect_text(text_content) + ' '
	text = processor.process( text.strip() )
	text += processor.collect_text( article.find( class_ = 'korjaus' ) )

    captions = processor.collect_image_captions( article.find_all( class_ = 'kuva') )

    return processor.create_dictionary('Pohjolan sanomat', url, 200, categories, datetime_list, author, title, ingress, text, [u''], captions)
