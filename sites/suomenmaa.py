import requests

from bs4 import BeautifulSoup

def parse( url ):

	# Somethin weird is going on with this site; check later

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	#for p in soup.find_all( class_='teksti' ):
	#	for string in p.stripped_strings:
	#    		out.write( string.encode('utf8') + ' ' )

	media_content = { 'url' : str( ''.encode('utf8') ),
					  'http' : str( http_status ).encode('utf8'),
					  'category' : str( ''.encode('utf8') ),
					  'date' : [''],
					  'time' : [''],
					  'title' : str( ''.encode('utf8') ),
					  'ingress' : str( ''.encode('utf8') ),
					  'text' : str( ''.encode('utf8') ),
					  'images' : [''],
					  'captions' : [''] }
	return media_content

if __name__ == '__main__':
	parse("http://www.suomenmaa.fi/etusivu/7399391.html", file('suomenmaa.txt', 'w'))
