import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

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

	out.write( content.encode('utf8') )

if __name__ == '__main__':

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
