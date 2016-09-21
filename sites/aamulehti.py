import requests

from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	for div in soup.find_all( 'div', {'class' : 'kuvavaraus-wrapper'} ):
		div.decompose()

	text = soup.find_all( class_ = 'Teksti' )
	content = text[0].get_text(' ', strip=True)
	content = process(content)

	out.write( content.encode('utf8') )

def process(content):
	content = content.replace(' .', '.')
	content = content.replace(' ,', ',')
	return content

if __name__ == '__main__':

	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/", file('aamulehti.txt', 'w'))
