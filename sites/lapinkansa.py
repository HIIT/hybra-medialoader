import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_ = 'Teksti' )

	for img in text[0].find_all( class_ = 'kuvavaraus-wrapper' ):
		img.decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.lapinkansa.fi/Lappi/1194944697007/artikkeli/kaunis+tykky+voi+olla+kavala+puille.html", file('lapinkansa.txt', 'w'))
