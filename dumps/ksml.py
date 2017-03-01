import time
import json
import pickle
import base64
import collections

import sys,os
sys.path.append( os.getcwd() )

import downloader
from sites import ksml as ksml_parser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, username, password):
    driver.get('https://media.portal.worldoftulo.com/Login?continue=https%3A%2F%2Fbackend.worldoftulo.com%2Foauth2%2Fauth%3Fclient_id%3D56b9cb80a672017f61000001%26redirect_uri%3Dhttp%253A%252F%252Fwww.ksml.fi%252Ftulo_sso_redirect.jsp%26state%3Dhttp%253A%252F%252Fwww.ksml.fi%252F%2523%26response_type%3Dcode%26oid%3Dmedia%26accountOrigin%3DKE')

    username_elem = driver.find_element_by_id( 'Username' )
    password_elem = driver.find_element_by_id( 'Password' )
    submit_btn = driver.find_element_by_xpath( '//input[@type="submit"]' )

    username_elem.send_keys( username )
    password_elem.send_keys( password )
    submit_btn.click()

    time.sleep(10)


def collect_urls(driver, year):
    driver.get( 'http://www.ksml.fi/arkisto/?tem=archive_lsearch5&dayfrom=' + year + '0101&dayto=' + year + '1231' )

    urls = []

    while True:

        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, 'neocontent'))
                )

        finally:
            remove_ad(driver, 'ESM_Tarranurkka')
            remove_ad(driver, 'ESM_Tikkeri')

            content = driver.find_element_by_id('neocontent')
            tags = content.find_elements_by_tag_name('a')

            for tag in tags:
                if 'search' in tag.get_attribute('href'):
                    continue
                urls.append(tag.get_attribute('href'))

            paginator = content.find_element_by_class_name('paginatorArchive')

            if 'Seuraava' not in paginator.find_elements_by_tag_name('a')[-1].get_attribute('innerHTML'):
                break
            else:
                paginator.find_elements_by_tag_name('a')[-1].click()

    save_urls( urls, year )

    return urls


def save_urls(urls, year):
    url_dir = 'saved_urls/'

    if not os.path.exists( url_dir ):
        os.makedirs( url_dir )

    try:
        url_log = open( url_dir + year + '.log', 'w' )

        for url in urls:

            url_log.write( url.replace('neo', 'arkisto/') + '\n' )

    except Exception, e:
        print e
        print "Error in saving urls " + year


def download(driver, url, raw_dir, error):
    driver.get(url.replace('neo', 'arkisto/'))

    try:
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'neocontent'))
            )

    finally:

        try:
            content = driver.find_element_by_id('neocontent')

            story = ksml_parser.parse_from_archive( url, content.get_attribute('innerHTML') )

            f = base64.encodestring( url )

            pickle.dump( story, open( raw_dir + f + '.pickle', 'w' ) )

            return story['http']

        except Exception, e:
            print e
            print "Failed " + url

            error.write( url + '\n' )


def remove_ad(driver, ad_id):
    try:
        ad = driver.find_element_by_id( ad_id )
        ad_images = ad.find_elements_by_tag_name('img')
        ad_images[0].click()

    except Exception, e:
        pass


if __name__ == '__main__':

    raw_dir = 'data-raw/' ## where pickles are stored
    data_dir = 'data/' ## where json outputs are stored
    error_dir = 'error-logs/' ## save error logs here

    for f in [raw_dir, data_dir, error_dir]:

        if not os.path.exists( f ):
            os.makedirs( f )

    driver = webdriver.Firefox()

    login( driver, sys.argv[1], sys.argv[2] )

    http_status = collections.defaultdict( int )

    for year in sys.argv[3:]:
        urls = collect_urls( driver, year )

        error = open( error_dir + 'error_' + year + '.log', 'w' )

        for url in urls:

            s = download( driver, url, raw_dir, error )

            http_status[ s ] += 1

    driver.quit()

    print 'Final status'
    for s, c in http_status.items():
        print s, '\t', c

    # regroup files to nicer folders
    store = downloader.resort_pickles( raw_dir )

    # store files as json
    for filename, data in store.items():
        json.dump( data , open(  data_dir + filename + '.json', 'w' ) )
