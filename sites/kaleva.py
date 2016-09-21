import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all('isense')

	for script in text[0].find_all('script'):
		script.decompose()

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.kaleva.fi/uutiset/kotimaa/asukkaat-vaativat-junille-nopeusrajoitusta-viime-yona-pamahti-niin-etta-pelkasin-hirren-menneen-poikki/683116/", file('kaleva.txt', 'w'))
