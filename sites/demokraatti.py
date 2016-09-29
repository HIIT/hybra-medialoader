import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='post-content' )

	text[0].find('ul', {'class' : 'single-post-date'}).decompose()
	text[0].find('div', {'class' : 'keywords-block'}).decompose()
	for div in text[0].find_all( 'div', {'class' : 'share-buttons-block'} ):
		div.decompose()
	text[0]('p')[-1].decompose()
	text[0].footer.decompose()

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	http_status = get_http_status( url )

	media_content = { 'url' : '', 'http' : str(http_status), 'category' : '', 'date' : [''], 'time' : [''], 'title' : '', 'ingress' : '', 'text' : '', 'images' : [''], 'captions' : ['']}
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

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
