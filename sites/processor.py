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
    content = content.replace(' '.decode('utf8'), ' ')
    content = content.replace('  '.decode('utf8'), '')
    return content

def create_dictionary(url, http_status, categories, datetime_list, author, title, ingress, text, images, captions):
    media_content = { 'url' : str( url.encode('utf8') ),
					  'http' : str( http_status ).encode('utf8'),
					  'categories' : categories,
					  'datetime_list' : datetime_list,
					  'author' : str( author.encode('utf8') ),
					  'title' : str( title.encode('utf8') ),
					  'ingress' : str( ingress.encode('utf8') ),
					  'text' : str( text.encode("utf8") ),
					  'images' : images,
					  'captions' : captions }
    return media_content

def decompose_scripts( article ):
    for script in article.find_all( 'script' ):
		script.decompose()

def collect_text( article, search_attribute, attribute_value ):
    if search_attribute == 'id':
        text = article.find( id = attribute_value )
    elif search_attribute == 'class':
        text = article.find( class_ = attribute_value )
    else:
        return ''

    text = text.get_text( ' ', strip=True )
    text = process(text)
    return text

def collect_images( article, url_base ):
    images = article.find_all( 'img' )
    image_src = [None]
    for img in images:
        image_src.append( '' + str( url_base + img['src'].encode('utf8') ) )
    image_src.pop(0)
    return image_src


def collect_image_captions( article, caption_css_class ):
    captions = article.find_all( class_ = caption_css_class )
    captions_text = [None]
    for caption in captions:
        captions_text.append( '' + str( caption.get_text(strip = True).encode('utf8') ) )
    captions_text.pop(0)
    return captions_text
