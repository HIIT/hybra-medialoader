import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='article-body' )

	for script in text[0].find_all('script'):
		script.decompose()
	for noscript in text[0].find_all('noscript'):
		noscript.decompose()
	text[0].find('div', {'class' : 'share-buttons'}).decompose()
	text[0].find('div', {'class' : 'subscribe-newsletter'}).decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.talouselama.fi/vaalit/vaalitebatti/murtuuko+suurten+puolueiden+valta++vaaliraati+vastaa/a2301513", file('talouselama.txt', 'w'))
