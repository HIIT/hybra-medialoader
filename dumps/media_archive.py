import time
import datetime
import json
import pickle
import base64
import collections
import importlib

import sys,os
sys.path.append( os.getcwd() )

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display


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

    time.sleep(1)


def get_source( driver, journal, interval ):

    source = {}

    try:
        driver.get('http://www.media-arkisto.com/ma/VisualBasic.php?query=&interval=' + interval + '&src=' + journal)

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hakutuloslyhennelmaots'))
            )

    except Exception, e:
        print e
        "Error in getting source."

    finally:

        try:
            search_results = driver.find_elements_by_class_name( 'hakutuloslyhennelmaots' )

            for result in search_results:
                if '</a>' not in result.get_attribute( 'innerHTML' ):
                    continue

                tag = result.find_element_by_tag_name( 'a' )

                query_domain = tag.get_attribute('innerHTML').lower().replace(' ', '_')
                query_url = tag.get_attribute( 'href' )

                source = {'domain' : query_domain, 'query' : query_url}

        except Exception, e:
            print e
            "Error in getting source."

    return source


def collect_urls( driver, source, page, error ):
    urls = []

    try:
        driver.get( source['query'] + '&page=' + str( page ) )

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'hakutuloslyhennelmaots'))
            )

    except Exception, e:
        print e
        "Error in collecting urls: " + source['domain'] + '_' + str(page)
        error.write("Error in collecting urls: " + source['domain'] + '_' + str(page) + '\n' )

    finally:

        try:
            search_results = driver.find_elements_by_class_name( 'hakutuloslyhennelmaots' )

            if not search_results:
                return urls

            for result in search_results:
                tag = result.find_element_by_tag_name( 'a' )
                urls.append( tag.get_attribute( 'href' ) )

        except Exception, e:
            print e
            "Error in collecting urls: " + source['domain'] + '_' + str(page)
            error.write("Error in collecting urls: " + source['domain'] + '_' + str(page) + '\n' )

    if urls:
        save_urls( urls, source['domain'], page )

    return urls


def save_urls(urls, domain, page):
    print "Saving urls: " + domain + ' page ' + str(page)

    url_dir = 'saved_urls/media_archive/'

    if not os.path.exists( url_dir ):
        os.makedirs( url_dir )

    try:
        url_log = open( url_dir + domain + '_' + str(page) + '.log', 'w' )

        for url in urls:
            url_log.write( url + '\n' )

    except Exception, e:
        print e
        print "Error in saving urls " + domain + '_' + str(page)


def collect_source( username, password, raw_dir, error, http_status ):

    page = 0
    downloaded = 0

    while( True ):
        driver = webdriver.Firefox()

        login( driver, username, password )

        source = get_source( driver, journal, interval )

        urls = collect_urls( driver, source, page, error )

        if not urls:
            break

        for url in urls:
            s = download( driver, url, source['domain'], raw_dir, error )

            downloaded += 1

            http_status[ s ] += 1

        driver.quit()

        print str(downloaded) + " stories downloaded from " + source['domain']

        page += 1

    return http_status


def format_for_download( domain ):
    domain_parts = domain.split('_')
    formatted_domain = ''

    for part in domain_parts:
        if not part[0].isdigit():
            formatted_domain += part

    return formatted_domain


def download( driver, url, domain, raw_dir, error ):

    try:
        driver.get( url )

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'artikkeli'))
            )

    except Exception, e:
        print e
        print "Error in downloading content: " + url
        error.write("Error in downloading content: " + url + '\n' )

    finally:

        try:
            domain = format_for_download( domain )

            parser = importlib.import_module('sites.' + domain)

            story = parser.parse_from_archive( url, element.get_attribute('innerHTML') )

            f = base64.encodestring( url )

            pickle.dump( story, open( raw_dir + f + '.pickle', 'w' ) )

            return story['http']

        except Exception, e:
            print e
            print "Error in downloading content: " + url
            error.write("Error in downloading content: " + url + '\n' )

            return story['http']


def resort_pickles( raw_dir ):

    store = collections.defaultdict( list )

    for d in os.listdir( raw_dir ):

        data = pickle.load( open( raw_dir + d ) )

        if int( data['http'] ) == 200:

            try:
                domain = data['domain'].replace(' ', '_').lower()

                time = max( data['datetime_list'] )

                destination = domain + '_' + str( time.year ) + '_' + str( time.month )
                data['datetime_list'] = map( str, data['datetime_list'] ) ## transform dateties to string

                store[ destination ].append( data ) ## TODO: potentially just directly write to file, if we run out of memory

            except Exception, e: ## sometimes not all data things are there, and thus let's prepeare for it
                print e

    return store


if __name__ == '__main__':

    stamp = datetime.datetime.now().isoformat().split('.')[0]

    raw_dir = 'data-raw/media_archive/' + stamp + '/' ## where pickles are stored
    data_dir = 'data/media_archive/' + stamp + '/' ## where json outputs are stored
    error_dir = 'error-logs/media_archive/' + stamp + '/' ## save error logs here

    for f in [raw_dir, data_dir, error_dir]:
        if not os.path.exists( f ):
            os.makedirs( f )

    display = Display(visible=0, size=(800, 600))
    display.start()

    username = sys.argv[1]
    password = sys.argv[2]

    http_status = collections.defaultdict( int )

    print "Collecting source: " + sys.argv[3] + ' ' + sys.argv[4]

    error = open( error_dir + 'error_' + sys.argv[3] + '_' + sys.argv[4] + '.log', 'w' )

    journal = sys.argv[3].title().replace(' ', '+') + '1'

    interval = sys.argv[4].replace('-', '+-+')

    http_status = collect_source( username, password, raw_dir, error, http_status )

    print 'Final status'
    for s, c in http_status.items():
        print s, '\t', c

    # regroup files to nicer folders
    store = resort_pickles( raw_dir )

    # store files as json
    for filename, data in store.items():
        json.dump( data , open(  data_dir + filename + '.json', 'w' ) )
