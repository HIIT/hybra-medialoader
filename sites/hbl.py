import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
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

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':

	parse("http://hbl.fi/nyheter/2014-12-03/690266/hawking-ai-kan-vara-slutet-oss", file('hbl.txt', 'w'))
