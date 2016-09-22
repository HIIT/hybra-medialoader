import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
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
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://www.ksml.fi/uutiset/ulkomaat/kalifornian-ennatyskuivuus-paattyi-rankkasateisiin/1944276", file('keski.txt', 'w'))
