# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime

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

def collect_datetime( html_element ):
    datetime_list = [None]

    if html_element != None:
        datetime_string_list = list_datetime_strings( html_element.get_text( ' ', strip = True ) )
        for string in datetime_string_list:
            if string != '':
                datetime_list.append( create_datetime_object( string ) )
            else:
                continue

    return prepare_datetime_list( datetime_list )

def collect_datetime_objects( html_elements ):
    datetime_list = [None]

    for element in html_elements:
        if element != None and element.has_attr( 'datetime' ):
            datetime_object = element['datetime'].replace('T', ' ').split( '+' )[0]
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
            captions_text.append( '' + process( caption.get_text( ' ', strip = True ) ) )
        else:
            continue
    captions_text.pop(0)
    return captions_text

def collect_categories_nav( html_elements ):
    categories = [None]
    for category in html_elements:
        if category != None:
            categories.append( process( category.get_text( strip = True ) ) )
        else:
            continue
    categories.pop(0)
    return categories

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

def list_datetime_strings( string ):
    string = remove_update_date_string( string )
    string = format_datetime_string( string )
    string_list = string.split( ' ' ) # Should split on the second occurrence if ' ' occurs more than once
    return string_list

def create_datetime_object( datetime_string ):
    datetime_parts = datetime_string.split( ' ' )
    if len( datetime_parts[0] ) < 7:
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

def remove_update_date_string( datetime_string ):
    datetime_string = datetime_string.replace( '(', '' )
    datetime_string = datetime_string.replace( ')', '' )
    datetime_string = datetime_string.replace( 'päivitetty:'.decode('utf8'), '' )
    datetime_string = datetime_string.replace( 'Päivitetty:'.decode('utf8'), '' )
    return datetime_string

def format_datetime_string( string ):
    string = string.replace( ' - ', ' ' )
    string = string.replace( '  ', ' ' )
    return string

def convert_month(month):
    conversions = { 'syyskuu' : '09' }
    return month.replace( month, conversions[month] )
