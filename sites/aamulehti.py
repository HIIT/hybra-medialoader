import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_ = 'Teksti' )

	for div in text[0].find_all( 'div', {'class' : 'kuvavaraus-wrapper'} ):
		div.decompose()

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':

	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/", file('aamulehti.txt', 'w'))
