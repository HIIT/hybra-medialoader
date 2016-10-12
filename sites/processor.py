# coding=utf8


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
