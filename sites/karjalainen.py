import requests

from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	teksti = soup.find_all( class_='itemBody' )

	for string in teksti[0].stripped_strings:
	        out.write( string.encode('utf8') + ' ' )

if __name__ == '__main__':
	parse("http://www.karjalainen.fi/uutiset/uutis-alueet/kotimaa/item/71016-arhinmaen-perheeseen-syntymassa-lapsi-puheenjohtaja-ei-osallistu-vaalitilaisuuksiin", file('karjalainen.txt', 'w'))
