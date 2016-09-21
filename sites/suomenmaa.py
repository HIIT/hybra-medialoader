import requests

from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	for p in soup.find_all( class_='teksti' ):
		for string in p.stripped_strings:
	    		out.write( string.encode('utf8') + ' ' )

if __name__ == '__main__':
	parse("http://www.suomenmaa.fi/etusivu/7399391.html", file('suomenmaa.txt', 'w'))
