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

	article = soup.find( 'article' )

	title = article.find( class_ = 'entry-title' ).get_text().strip()
	date = [ str( article.find( class_ = 'postmeta-date' ).get_text(' ', strip = True).encode('utf8') ) ]

	text = article.find_all( class_= 'entry-content' )
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', title, '', text, [''], [''])

if __name__ == '__main__':

	parse("http://blogit.iltalehti.fi/eija-riitta-korhola/2015/03/15/visioni-helsingista-kansainvalinen-metropoli/", file('blogit.txt', 'w'))
