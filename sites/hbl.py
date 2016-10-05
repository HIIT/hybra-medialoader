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

	text = soup.find_all( 'article' )
	text[0].find( id = 'articleimages' ).decompose()
	text[0]('p')[-1].decompose()
	text[0].find( id = 'nodefooter' ).decompose()
	text[0].find( id = 'page-title' ).decompose()
	text[0].find( id = 'publishedinfo' ).decompose()
	text[0].find( id = 'article-controls' ).decompose()
	for script in text[0].find_all('script'):
		script.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://hbl.fi/nyheter/2014-12-03/690266/hawking-ai-kan-vara-slutet-oss", file('hbl.txt', 'w'))
