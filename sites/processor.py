# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

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

def convert_month(month):
    conversions = { 'syyskuu' : '09' }
    return month.replace( month, conversions[month] )

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

def decompose( html_element ):
    html_element.decompose()


def decompose_all( html_elements ):
    for element in html_elements:
        element.decompose()

def collect_text( html_element ):
    text = html_element.get_text( ' ', strip=True )
    text = process(text)
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
        image_src.append( '' + str( url_base + image_link['href'].encode('utf8') ) )
    image_src.pop(0)
    return image_src

def collect_image_captions( captions ):
    captions_text = [None]
    for caption in captions:
        captions_text.append( '' + process( caption.get_text( ' ', strip = True ) ) )
    captions_text.pop(0)
    return captions_text

def collect_categories_nav( html_elements ):
    categories = [None]
    for category in html_elements:
        categories.append( process( category.get_text( strip = True ) ) )
    categories.pop(0)
    return categories
