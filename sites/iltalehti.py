import requests
import processor
from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'iso-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( 'isense' )

	text[0].find('div', {'class' : 'kainalo'}).decompose()
	text[0].find('div', {'class' : 'author'}).decompose()
	text[0].find('div', {'class' : 'kp-share-area'}).decompose()

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':

	parse("http://www.iltalehti.fi/uutiset/2014120218885176_uu.shtml", file('iltalehti.txt', 'w'))
