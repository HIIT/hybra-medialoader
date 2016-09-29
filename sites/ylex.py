import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	r = requests.get( url )

    http_status = r.status_code
	if r.status_code == 404:
		return

    ## ylex seems to be JS single page application; this approach can't handle it. just return here

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
	parse("http://yle.fi/ylex/uutiset/ylexaan_tulossa_politiikan_superviikot__myos_sina_voit_tentata_paattajia_ennen_vaaleja/3-7875448", file('yle.txt', 'w'))
