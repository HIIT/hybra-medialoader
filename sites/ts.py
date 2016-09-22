import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='tsv3-c-common-article__textitem tsv3-c-common-article__textitem--teksti' )

	for script in text[0].find_all( 'script' ):
		script.decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.ts.fi/eduskuntavaalit/750980/Start+up+yrittaja+kuplii+innostusta", file('ts.txt', 'w'))
