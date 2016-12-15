# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
import re

"""A module encapsulating the functions used by the media parsers to scrape data from websites."""

def decompose( html_element ):
    """Decomposes a html element if the element's type is not None.

    Parameters:
        html_element - A BeautifulSoup tag.
    """
    if html_element != None:
        html_element.decompose()
    else:
        return

def decompose_all( html_elements ):
    """Iterates over a list of html elements and decomposes the elements if their type is not None.

    Parameters:
        html_elements - A list of BeautifulSoup tags.
    """
    for element in html_elements:
        if element != None:
            element.decompose()
        else:
            continue

def collect_categories( html_elements, decompose ):
    """Iterates over a list of html elements and collects their contained text using the collect_text() function.

    Returns the collected texts as a list of strings.

    Parameters:
        html_elements - A list of BeautifulSoup tags.
        decompose - A boolean determining whether the html elements should be decomposed after handling.
    """
    categories = [None]

    for element in html_elements:
        if element != None:
            categories.append( collect_text( element, decompose ) )

    categories.pop(0)
    return categories

def collect_datetime( html_element, datetime_format ):
    """Collects all datetime strings contained within a html element using the re module,
    and returns them as a list of datetime objects.

    Uses the list_datetime_objects() function to create the datetime object list from datetime strings.

    Parameters:
        html_element - A BeautifulSoup tag containing datetime strings.
        datetime_format - A string determining the format of the datetime strings on the website.
    """
    if datetime_format == 'timedate':
        datetime_expression = r'([0-2]?[0-9][.:][0-6][0-9])[^0-9]*([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)'
    elif datetime_format == 'datetime date':
        datetime_expression = r'([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)?[^0-9]*([0-2]?[0-9][.:][0-6][0-9])?'
    else:
        datetime_expression = r'([0-3]?[0-9]\.[0-1]?[0-9]\.[1-2]?[09]?[0-9]?[0-9]?)[^0-9]*([0-2]?[0-9][.:][0-6][0-9])?'

    datetime_list = []
    if html_element != None:
        datetime_string = html_element.get_text( ' ' , strip = True )
        match_list = re.findall( datetime_expression, datetime_string )
        datetime_list = list_datetime_objects( match_list, datetime_format )

    return datetime_list

def collect_datetime_objects( html_elements, attribute ):
    """Iterates over a list of html_elements and returns their timestamp attributes as a list of datetime objects.

    Uses the function prepare_datetime_list().

    Parameters:
        html_elements - A list of BeautifulSoup tags.
        attribute - A string name of the html element attribute containing the timestamp.
    """
    datetime_list = [None]

    for element in html_elements:
        if element != None and element.has_attr( attribute ):
            datetime_object = element[attribute].replace('T', ' ').replace('Z', '')
            datetime_object = datetime_object.split( '+' )[0].split('.')[0]
            datetime_list.append( datetime_object )
        else:
            continue

    return prepare_datetime_list( datetime_list )

def collect_datetime_json( json, published, updated ):
    """Collects the publish and update datetime objects from json and returns them as a list.

    Parameters:
        json - JSON containing the publish and update datetime objects.
        published - A string name of the attribute in the JSON with the publish datetime as its value.
        updated - A string name of the attribute in the JSON with the update datetime as its value.
    """
    datetime_list = [None]
    if published in json:
        datetime_list.append( strip_datetime_object( json[published] ) )
    if updated in json:
        datetime_list.append( strip_datetime_object( json[updated] ) )
    return prepare_datetime_list( datetime_list )

def collect_text( html_element, decompose ):
    """Returns the text contained in a html element if the type of the element is not None.

    Uses the function process().

    Parameters:
        html_element - A BeautifulSoup tag containing the text.
        decompose - A boolean determining whether the html elements should be decomposed after handling.
    """
    if html_element != None:
        text = html_element.get_text( ' ', strip=True )
        text = process(text)

        if decompose == True:
            html_element.decompose()
    else:
        text = ''

    return text

def collect_images( images, attribute, url_base ):
    """Iterates over a list of html image elements and returns their corresponding urls as a list of strings.

    Parameters:
        images - A list of BeautifulSoup tags.
        attribute - A string that gives the image element attribute which contains the image's url.
        url_base - A string that gives the base part of the image urls.
    """
    image_src = [None]
    for img in images:
        if img != None and img.has_attr( attribute ):
            image_src.append( '' + str( url_base + img[attribute].encode('utf8') ) )
    image_src.pop(0)
    return image_src

def collect_images_by_parent( html_elements, url_base ):
    """Iterates over a list of html elements containing image hyperlinks and collects their urls.

    Parameters:
        html_elements - A list of BeautifulSoup tags.
        url_base - A string that gives the base part of the image urls.
    """
    image_src = [None]
    for parent in html_elements:
        image_link = parent.find( 'a' )
        if image_link != None:
            image_src.append( '' + str( url_base + image_link['href'].encode('utf8') ) )
        else:
            continue
    image_src.pop(0)
    return image_src

def collect_image_captions( captions, decompose = False ):
    """Iterates over a list of html elements containing image captions and returns them as a list of strings.

    Uses the function collect_text().

    Parameters:
        captions - A list of BeautifulSoup tags containing the caption texts.
        decompose - A boolean determining whether the html elements should be decomposed after handling.
    """
    captions_text = [None]
    for caption in captions:
        if caption != None:
            captions_text.append( '' + collect_text( caption, decompose ) )

    captions_text.pop(0)
    return captions_text

def list_datetime_objects( match_list, datetime_format ):
    """Iterates over a list of datetime strings and returns a list of datetime objects created from them.

    Uses the functions create_datetime_object() and prepare_datetime_list().

    Parameters:
        match_list - A list containing datetime strings.
        datetime_format - A string determining the format of the datetime strings on the website.
    """
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
    """Returns a datetime object created from a datetime string.

    Parameters:
        datetime_string - A datetime in string format.
    """
    datetime_parts = datetime_string.split( ' ' )
    if len( datetime_parts[0] ) < 7 :
        datetime_parts[0] = datetime_parts[0] + '2016'

    if len( datetime_parts ) > 1:
        datetime_parts[1] = datetime_parts[1].replace( ':', '.' )
        datetime_object = datetime.strptime( datetime_parts[0] + ' ' + datetime_parts[1], '%d.%m.%Y %H.%M' )
    else:
        datetime_object = datetime.date( datetime.strptime( datetime_parts[0], '%d.%m.%Y' ) )
    return datetime_object

def strip_datetime_object( datetime_object ):
    """Formats a datetime object and returns the formatted object.

    Parameters:
        datetime_object - A datetime object to format.
    """
    datetime_object = datetime_object.replace('T', ' ').replace('Z', '')
    datetime_object = datetime_object.split( '+' )[0].split('.')[0]
    return datetime_object

def prepare_datetime_list( datetime_list ):
    """Removes the first member of a datetime_list and returns the list reversed.

    Parameters:
        datetime_list - A list of datetime objects.
    """
    datetime_list.pop(0)
    datetime_list.reverse()
    return datetime_list

def create_dictionary(url, http_status, categories, datetime_list, author, title, ingress, text, images, captions):
    """Returns a dictionary containing the scraped data from the website, given as parameters.

    Parameters:
        url - The website url as a string object.
        http_status - The parser http request status.
        categories - A list of collected news item categories as strings.
        datetime_list - A list of datetime objects.
        author - The author of the news item as a string.
        title - The title of the news item as a string.
        ingress - The ingress of the news item as a string.
        text - The main text content of the news item as a string.
        images - A list of the source urls of the images in the news item as strings.
        captions - A list of the image captions in the news item as strings.
    """
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
    """Performs character replace functions on scraped text and returns the text as a string.

    Parameters:
        content - Content text scraped from a website.
    """
    content = content.replace(' .', '.')
    content = content.replace(' ,', ',')
    content = content.replace('( ', '(')
    content = content.replace(' )', ')')
    content = content.replace(' !', '!')
    content = content.replace(' ?', '?')
    content = content.replace(' ;', ';')
    content = content.replace(' ]', ']')
    content = content.replace('[ ', '[')
    content = content.replace('   ', ' ')
    content = content.replace('    ', '')
    content = content.replace('      ', ' ' )
    content = content.replace('\n', ' ')
    content = content.replace(' '.decode('utf8'), ' ')
    content = content.replace('  '.decode('utf8'), ' ')
    return str( content.encode('utf8') )

def convert_month(datetime_string):
    """Converts month substrings in a datetime string into their numeral equivalents.

    Parameters:
        datetime_string - A string expressing a datetime.
    """
    conversions = { 'syyskuu' : '09' }
    for conversion in conversions:
        datetime_string = datetime_string.replace( conversion, conversions[conversion] )
    return datetime_string
