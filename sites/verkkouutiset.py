import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	ingress = soup.find_all( class_ = 'ingress')
	text = soup.find_all( class_='articlepart-1' )

	for slides in text[0].find_all( class_ ='flexslider'):
		slides.decompose()

	content = ingress[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
