import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='article-single-section__content' )

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.maaseuduntulevaisuus.fi/maatalous/nurmipelloille-voi-tulla-k%C3%A4ytt%C3%B6rajoituksia-1.76216", file('maaseudun.txt', 'w'))
