import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='views-field views-field-body' )
	
	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
