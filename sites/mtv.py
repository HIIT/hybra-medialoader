import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	lead = soup.find_all( class_ = 'lead-paragraph' )
	text = soup.find_all( class_ = 'editorial' )

	for ad in text[0].find_all( class_ = 'ad' ):
		ad.decompose()

	content = lead[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.mtv.fi/uutiset/kotimaa/artikkeli/jarjesto-sipilaan-kohdistuneesta-uhkailusta-iltapaivalehdissa-lausunto-hammastyttaa/4918590", file('mtv.txt', 'w'))
