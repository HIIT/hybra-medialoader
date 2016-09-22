import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='post-content span8' )

	for script in text[0].find_all( 'script' ):
		script.decompose()
	text[0].find('p', {'class' : 'article-page-writer'}).decompose()
	text[0].find('div', {'class' : 'somebar'}).decompose()
	text[0].find('div', {'class' : 'tags'}).decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("https://www.suomenuutiset.fi/perussuomalaiset-hurjassa-nosteessa-puoluesihteeri-ei-yllattynyt/", file('suomenuutiset.txt', 'w'))
