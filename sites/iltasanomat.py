import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	ingress = soup.find_all( class_='ingress')
	text = soup.find_all( class_='body' )

	for script in text[0].find_all('script'):
		script.decompose()

	for url in text[0].find_all('span', {'class' : 'print-url'}):
		url.decompose()

	content = ingress[0].get_text(' ', strip=True)
	content += ' ' + text[0].get_text(' ', strip=True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.iltasanomat.fi/ulkomaat/art-1288789081654.html", file('iltasa.txt', 'w'))
