import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	api_path = 'http://yle.fi/ylex/api/article/'

	_id = url.split( url )[-1]

	r = requests.get( api_path + _id )
	r = r.json()

	http_status = r.status_code
	if r.status_code == 404:
		return

	## ylex seems to be JS single page application; this approach can't handle it. just return here
	authors = map( labda x:['name'] , r['authors'] )
	return processor.create_dictionary(url, http_status, r['homesection']['name'], [ r['dateModified'], r['datePublished'] ], [''], authors, r['title'], r['lead'], r['text'], [''], [''])

if __name__ == '__main__':
	parse("http://yle.fi/ylex/uutiset/ylexaan_tulossa_politiikan_superviikot__myos_sina_voit_tentata_paattajia_ennen_vaaleja/3-7875448", file('yle.txt', 'w'))
