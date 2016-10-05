import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	summary = soup.find_all( class_ = 'article__summary' )
	text = soup.find_all( class_='article__body' )
	for script in text[0].find_all( 'script' ):
		script.decompose()
	for i in range(0, 3):
		text[0]('p')[-1].decompose()
	content = summary[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	text = processor.process(content)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.ksml.fi/uutiset/ulkomaat/kalifornian-ennatyskuivuus-paattyi-rankkasateisiin/1944276", file('keski.txt', 'w'))
