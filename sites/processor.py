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

def decompose_scripts( soup ):
    for script in soup.find_all( 'script' ):
		script.decompose()

def collect_text( soup, search_attribute, attribute_value ):
    if search_attribute == 'id':
        text = soup.find( id = attribute_value )
    elif search_attribute == 'class':
        text = soup.find( class_ = attribute_value )
    elif attribute_value == '':
        text = soup.find( search_attribute )

    text = text.get_text( ' ', strip=True )
    text = process(text)
    return text

def collect_images( soup, parent_element_class, url_base ):
    if ( parent_element_class != '' ):
        return collect_images_by_parent( soup, parent_element_class, url_base )

    images = soup.find_all( 'img' )
    image_src = [None]
    for img in images:
        image_src.append( '' + str( url_base + img['src'].encode('utf8') ) )
    image_src.pop(0)
    return image_src

def collect_images_by_parent( soup, parent_element_class, url_base ):
    images = soup.find_all( class_ = parent_element_class )
    image_src = [None]
    for img in images:
        image_link = img.find( 'a' )
        image_src.append( '' + str( url_base + image_link['href'].encode('utf8') ) )
    image_src.pop(0)
    return image_src

def collect_image_captions( soup, search_attribute, attribute_value ):
    if search_attribute == 'class':
        captions = soup.find_all( class_ = attribute_value )
    elif search_attribute == 'itemprop':
        captions = soup.find_all( itemprop = attribute_value )
    elif attribute_value == '':
        captions = soup.find_all( search_attribute )

    captions_text = [None]
    for caption in captions:
        captions_text.append( '' + str( process( caption.get_text( ' ', strip = True ) ).encode('utf8') ) )
    captions_text.pop(0)
    return captions_text

def collect_categories_nav( soup, category_css_class ):
    categories = [None]
    categories_data = soup.find_all( class_ = category_css_class )
    for category in categories_data:
        categories.append( str( category.get_text( strip = True ).encode('utf8') ) )
    categories.pop(0)
    return categories
