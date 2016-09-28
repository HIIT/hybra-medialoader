import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	http_status = get_http_status( url )

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'article-content')
	article.find( class_ = 'related-articles-container' ).decompose()

	title = str( article.find( class_ = 'Otsikko' ).get_text().strip().encode('utf8') )

	category = str( article.find( class_ = 'category' ).get_text().strip() )

	meta = article.find( class_ = 'post-meta' )
	meta.find( class_ = 'category' ).decompose()
	meta.find( class_ = 'updated' ).decompose()

	meta_list = [None] * 4
	i = 0
	for string in meta.stripped_strings:
		meta_list[i] = string
		i += 1
	date = [str( meta_list[2] ), str( meta_list[0] )]
	time = [str( meta_list[3] ), str( meta_list[1] )]

	images = article.find_all( 'img' )
	image_src = [None] * len(images)
	i = 0
	for img in images:
		image_src[i] = str( img['src'] )
		i += 1

	captions = article.find_all( class_ = 'caption' )
	captions_text = [None] * len(captions)
	i = 0
	for caption in captions:
		captions_text[i] = str( caption.get_text().encode('utf8') )
		i += 1

	text = article.find( class_ = 'Teksti' )
	for div in text.find_all( class_ = 'kuvavaraus-wrapper' ):
		div.decompose()
	text = text.get_text(' ', strip = True)
	text = processor.process(text)
	text = str( text.encode('utf8') )

	media_content = { 'url' : url, 'http' : str(http_status), 'category' : category, 'date' : date, 'time' : time, 'title' : title, 'ingress' : '', 'text' : text, 'images' : image_src, 'captions' : captions_text}

	return media_content

def get_http_status( url ):
	r = requests.head( url )
	return r.status_code

def write_file( out, content ):
	file_content = content['url'].encode('utf8') + "\n"
	file_content += content['http'] + "\n"
	file_content += content['category'].encode('utf8') + "\n"

	for date in content['date']:
		file_content += date.encode('utf8') + "\n"
	for time in content['time']:
		file_content += time.encode('utf8') + "\n"

	file_content += content['title'] + "\n"
	file_content += content['ingress'].encode('utf8') + "\n"
	file_content += content['text'] + "\n"

	for img in content['images']:
		file_content += img.encode('utf8') + "\n"
	for caption in content['captions']:
		file_content += caption + "\n"

	out.write( file_content.strip() )

if __name__ == '__main__':

	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/", file('aamulehti.txt', 'w'))
