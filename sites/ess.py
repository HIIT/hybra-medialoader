import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'mainArticle-content-wrapper' )
	header = article.find( id = 'main-article-header' )

	category = header.find( class_ = 'section' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	published = header.find( class_ = 'publish-date' ).get_text( strip = True )
	updated = header.find( class_ = 'updated-date' )
	if ( type(updated) != None ):
		updated = updated.get_text( strip = True )
		updated = updated.split(' ')
	datetime_list = [datetime.date(datetime.strptime(updated[1], "%d.%m.%Y")), datetime.date(datetime.strptime(published, "%d.%m.%Y"))]

	author = article.find( class_ = 'authorName' ).get_text( strip = True )

	title = article.find( class_ = 'main-article-header' ).get_text( strip = True )

	text = soup.find_all( class_='body' )
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	article.find( class_ = 'authorPicture' ).decompose()
	images = article.find_all( 'img' )
	image_src = [None] * len(images)
	i = 0
	for img in images:
		image_src[i] = str( img['src'].encode('utf8') )
		i += 1

	captions = article.find_all( class_ = 'main-media-caption' )
	captions_text = [None] * len(captions)
	i = 0
	for caption in captions:
		captions_text[i] = str( caption.get_text(strip = True).encode('utf8') )
		i += 1

	return processor.create_dictionary(url, http_status, categories, datetime_list, author, title, '', text, image_src, captions_text)

if __name__ == '__main__':

	parse("http://www.ess.fi/uutiset/talous/2014/12/03/perinteikas-konepaja-kaatui-venajan-kauppaan?ref=uutiset-section-teaser-latestCurrent-teaserCategoryMain", file('ess.txt', 'w'))
