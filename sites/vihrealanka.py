import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_ = 'node-wrap' )

	text[0].find('h1').decompose()
	text[0].find(class_ = 'juttutiedot').decompose()
	text[0].find(class_ = 'blogaajantiedot').decompose()
	for script in text[0].find_all('script'):
		script.decompose()
	text[0].find(class_ = 'avainsanat').decompose()
	text[0].find(class_ = 'twitter-share-button').decompose()
	text[0].find(class_ = 'fb-like').decompose()
	text[0].find(class_ = 'node-wrap').decompose()
	for div in text[0].find_all(class_ = 'tyrkkyBox'):
		div.decompose()
	text[0]('h4')[-1].decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	media_content = { 'url' : str( ''.encode('utf8') ),
					  'http' : str( http_status ).encode('utf8'),
					  'category' : str( ''.encode('utf8') ),
					  'date' : [''],
					  'time' : [''],
					  'title' : str( ''.encode('utf8') ),
					  'ingress' : str( ''.encode('utf8') ),
					  'text' : str( ''.encode('utf8') ),
					  'images' : [''],
					  'captions' : [''] }
	return media_content

if __name__ == '__main__':
	parse("http://www.vihrealanka.fi/blogi-eno-vastaa/onko-tonnikalassa-myrkkyj%C3%A4", file('vihrealanka.txt', 'w'))
