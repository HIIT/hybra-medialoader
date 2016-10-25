# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
import re

def decompose( html_element ):
    if html_element != None:
        html_element.decompose()
    else:
        return

def decompose_all( html_elements ):
    for element in html_elements:
        if element != None:
            element.decompose()
        else:
            continue

def collect_categories( html_elements ):
    categories = [None]

    for element in html_elements:
        if element != None:
            categories.append( collect_text( element ) )

    categories.pop(0)
    return categories

def collect_datetime( html_element, datetime_format ):
    if datetime_format == 'timedate':
        datetime_expression = r'([0-2]?[0-9][.:][0-6][0-9])[^0-9]*([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)'
    elif datetime_format == 'datetime date':
        datetime_expression = r'([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)?[^0-9]*([0-2]?[0-9][.:][0-6][0-9])?'
    else:
        datetime_expression = r'([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)[^0-9]*([0-2]?[0-9][.:][0-6][0-9])?'

    if html_element != None:
        datetime_string = html_element.get_text( ' ' , strip = True )
        match_list = re.findall( datetime_expression, datetime_string )
        datetime_list = list_datetime_objects( match_list, datetime_format )

    return datetime_list

def collect_datetime_objects( html_elements, attribute ):
    datetime_list = [None]

    for element in html_elements:
        if element != None and element.has_attr( attribute ):
            datetime_object = element[attribute].replace('T', ' ').replace('Z', '')
            datetime_object = datetime_object.split( '+' )[0].split('.')[0]
            datetime_list.append( datetime_object )
        else:
            continue

    return prepare_datetime_list( datetime_list )

def collect_text( html_element ):
    if html_element != None:
        text = html_element.get_text( ' ', strip=True )
        text = process(text)
    else:
        text = ''
    return text

def collect_images( images, url_base ):
    image_src = [None]
    for img in images:
        image_src.append( '' + str( url_base + img['src'].encode('utf8') ) )
    image_src.pop(0)
    return image_src

def collect_images_by_parent( html_elements, url_base ):
    image_src = [None]
    for parent in html_elements:
        image_link = parent.find( 'a' )
        if image_link != None:
            image_src.append( '' + str( url_base + image_link['href'].encode('utf8') ) )
        else:
            continue
    image_src.pop(0)
    return image_src

def collect_image_captions( captions ):
    captions_text = [None]
    for caption in captions:
        if caption != None:
            captions_text.append( '' + collect_text( caption ) )

    captions_text.pop(0)
    return captions_text

def list_datetime_objects( match_list, datetime_format ):
    datetime_list = [None]
    published_date = ''
    for match in match_list:
        if datetime_format == 'timedate':
            date = match[1]
            time = match[0]
        else:
            date = match[0]
            time = match[1]

        if date == '' and time == '':
            continue
        elif date == '':
            datetime_list.append( create_datetime_object( published_date + ' ' + time ) )
        elif time == '':
            datetime_list.append( create_datetime_object( date ) )
        else:
            datetime_list.append( create_datetime_object( date + ' ' + time ) )
            published_date = date

    return prepare_datetime_list( datetime_list )

def create_datetime_object( datetime_string ):
    datetime_parts = datetime_string.split( ' ' )
    if len( datetime_parts[0] ) < 7 :
        datetime_parts[0] = datetime_parts[0] + '2016'

    if len( datetime_parts ) > 1:
        datetime_parts[1] = datetime_parts[1].replace( ':', '.' )
        datetime_object = datetime.strptime( datetime_parts[0] + ' ' + datetime_parts[1], '%d.%m.%Y %H.%M' )
    else:
        datetime_object = datetime.date( datetime.strptime( datetime_parts[0], '%d.%m.%Y' ) )
    return datetime_object

def prepare_datetime_list( datetime_list ):
    datetime_list.pop(0)
    datetime_list.reverse()
    return datetime_list

def create_dictionary(url, http_status, categories, datetime_list, author, title, ingress, text, images, captions):
    media_content = { 'url' : url,
					  'http' : str( http_status ),
					  'categories' : categories,
					  'datetime_list' : datetime_list,
					  'author' : author,
					  'title' : title,
					  'ingress' : ingress,
					  'text' : text,
					  'images' : images,
					  'captions' : captions }
    return media_content

def process(content):
    content = content.replace(' .', '.')
    content = content.replace(' ,', ',')
    content = content.replace('( ', '(')
    content = content.replace(' )', ')')
    content = content.replace(' !', '!')
    content = content.replace(' ?', '?')
    content = content.replace(' ;', ';')
    content = content.replace(' ]', ']')
    content = content.replace('[ ', '[')
    content = content.replace('    ', '')
    content = content.replace('\n', ' ')
    content = content.replace(' '.decode('utf8'), ' ')
    content = content.replace('  '.decode('utf8'), '')
    content = str( content.encode('utf8') )
    return content

def convert_month(datetime_string):
    conversions = { 'syyskuu' : '09' }
    for conversion in conversions:
        datetime_string = datetime_string.replace( conversion, conversions[conversion] )
    return datetime_string
