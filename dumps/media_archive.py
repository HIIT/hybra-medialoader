import time
import json
import pickle
import base64
import collections

import sys,os
sys.path.append( os.getcwd() )

import downloader

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from pyvirtualdisplay import Display


def login(driver, username, password):
    driver.get('http://www.media-arkisto.com/Login.php')

    form = driver.find_element_by_class_name( 'hakuformbg' )

    inputs = form.find_elements_by_tag_name( 'input' )

    username_elem = inputs[0]
    password_elem = inputs[1]
    submit_btn = inputs[2]

    username_elem.send_keys( username )
    password_elem.send_keys( password )
    submit_btn.click()

    time.sleep(10)


def get_sources( driver ):
    sources = []

    driver.get('http://www.media-arkisto.com/ma/VisualBasic.php?query=&interval=all&src=Kaikki1&Kysy.x=32&Kysy.y=11')
    search_results = driver.find_elements_by_class_name( 'hakutuloslyhennelmaots' )

    for result in search_results:
        if '</a>' not in result.get_attribute( 'innerHTML' ):
            continue

        tag = result.find_element_by_tag_name( 'a' )

        query_domain = tag.get_attribute('innerHTML').lower().replace(' ', '_')
        query_url = tag.get_attribute( 'href' )

        sources.append( {'domain' : query_domain, 'query' : query_url} )

    return sources


def collect_urls( driver, query, page ):
    urls = []
    driver.get( query + str( page ) )


def collect_source( driver, source, raw_dir ):
    print "Collecting source: " + source['domain']

    page = 0
    downloaded = 0

    while( True ):
        urls = collect_urls( driver, source['query'], page )

        if not urls:
            break

        for url in urls:
            download( driver, url, raw_dir )
            downloaded += 1

        print str(downloaded) + " stories downloaded from " + source['domain']

        page += 1


def download( driver, url, raw_dir ):
    pass


if __name__ == '__main__':

    raw_dir = 'data-raw/' ## where pickles are stored
    data_dir = 'data/' ## where json outputs are stored
    error_dir = 'error-logs/' ## save error logs here

    for f in [raw_dir, data_dir, error_dir]:

        if not os.path.exists( f ):
            os.makedirs( f )

    #display = Display(visible=0, size=(800, 600))
    #display.start()

    driver = webdriver.Firefox()

    login( driver, sys.argv[1], sys.argv[2] )

    query_sources = get_sources( driver )

    for source in query_sources:
        collect_sources( source, raw_dir )

    driver.quit()
