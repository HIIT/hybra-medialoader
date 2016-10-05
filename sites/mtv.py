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

	lead = soup.find_all( class_ = 'lead-paragraph' )
	text = soup.find_all( class_ = 'editorial' )
	for ad in text[0].find_all( class_ = 'ad' ):
		ad.decompose()
	content = lead[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	text = processor.process(content)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.mtv.fi/uutiset/kotimaa/artikkeli/jarjesto-sipilaan-kohdistuneesta-uhkailusta-iltapaivalehdissa-lausunto-hammastyttaa/4918590", file('mtv.txt', 'w'))
