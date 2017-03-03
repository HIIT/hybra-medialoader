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

from pyvirtualdisplay import Display


def login(driver, username, password):
    driver.get('https://media.portal.worldoftulo.com/Login?continue=https%3A%2F%2Fbackend.worldoftulo.com%2Foauth2%2Fauth%3Fclient_id%3D56b9cb80a672017f61000001%26redirect_uri%3Dhttp%253A%252F%252Fwww.ksml.fi%252Ftulo_sso_redirect.jsp%26state%3Dhttp%253A%252F%252Fwww.ksml.fi%252F%2523%26response_type%3Dcode%26oid%3Dmedia%26accountOrigin%3DKE')

    username_elem = driver.find_element_by_id( 'Username' )
    password_elem = driver.find_element_by_id( 'Password' )
    submit_btn = driver.find_element_by_xpath( '//input[@type="submit"]' )

    username_elem.send_keys( username )
    password_elem.send_keys( password )
    submit_btn.click()

    time.sleep(10)


def collect_urls(driver, start_date, end_date):
    print "Collecting urls: " + start_date + '...' + end_date

    driver.get( 'http://www.ksml.fi/arkisto/?tem=archive_lsearch5&dayfrom=' + start_date + '&dayto=' + end_date )
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

            print str(len(urls)) + ' urls collected...'

            if 'Seuraava' not in paginator.find_elements_by_tag_name('a')[-1].get_attribute('innerHTML'):
                break
            else:
                paginator.find_elements_by_tag_name('a')[-1].click()

    save_urls( urls, start_date, end_date )

    return urls


def save_urls(urls, start_date, end_date):
    print "Saving urls: " + start_date + '...' + end_date

    url_dir = 'saved_urls/'

    if not os.path.exists( url_dir ):
        os.makedirs( url_dir )

    try:
        url_log = open( url_dir + start_date + '_' + end_date + '.log', 'w' )

        for url in urls:
            url_log.write( url.replace('neo', 'arkisto/') + '\n' )

    except Exception, e:
        print e
        print "Error in saving urls " + start_date + '...' + end_date


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


def split_to_months(year):

    leap_years = ['1996', '2000', '2004', '2008', '2012', '2016']

    feb_end = '0228'
    if year in leap_years:
        feb_end = '0229'

    if year == '2017':
        return {'0101' : '0131', '0201' : feb_end, '0301' : '0302'}

    periods = {'0101' : '0131',
               '0201' : feb_end,
               '0301' : '0331',
               '0401' : '0430',
               '0501' : '0531',
               '0601' : '0630',
               '0701' : '0731',
               '0801' : '0831',
               '0901' : '0930',
               '1001' : '1031',
               '1101' : '1130',
               '1201' : '1231'
               }

    return periods


if __name__ == '__main__':

    raw_dir = 'data-raw/ksml/' ## where pickles are stored
    data_dir = 'data/ksml/' ## where json outputs are stored
    error_dir = 'error-logs/ksml/' ## save error logs here

    for f in [raw_dir, data_dir, error_dir]:
        if not os.path.exists( f ):
            os.makedirs( f )

    display = Display(visible=0, size=(800, 600))
    display.start()

    profile = webdriver.FirefoxProfile('/home/juhopaak/selenium_tmp/')

    driver = webdriver.Firefox(profile)

    login( driver, sys.argv[1], sys.argv[2] )

    http_status = collections.defaultdict( int )

    for year in sys.argv[3:]:
        months = split_to_months( year )

        for start, end in months.items():
            start_date = year + start
            end_date = year + end

            urls = collect_urls( driver, start_date, end_date )

            print str( len(urls) ) + " urls collected: " + start_date + '...' + end_date
            print "Downloading content: " + start_date + '...' + end_date

            error = open( error_dir + 'error_' + start_date + '_' + end_date + '.log', 'w' )

            downloaded = 0

            for url in urls:
                s = download( driver, url, raw_dir, error )

                downloaded += 1

                print str(downloaded) + " stories downloaded from " + start_date + '...' + end_date

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
