import time
import datetime
import json
import pickle
import base64
import collections
from webdriver_timer import Timeout

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


def collect_period(start_date, end_date, http_status, error):
    print "Collecting period: " + start_date + '...' + end_date

    pagination = 1
    downloaded = 0

    while True:

        try:
            print "Trying to start new browser instance on page " + str(pagination) + "..."
            with Timeout(40):
                driver = webdriver.Firefox()
        except Exception, e:
            print "Error in starting browser instance on page " + str(pagination) + ': ' + repr(e)
            error.write("Error in starting browser instance on page " + str(pagination) + ': ' + repr(e) + '\n' )
            continue

        if not login( driver, username, password, error): continue

        try:
            driver.get( 'http://www.ksml.fi/arkisto/?tem=archive_lsearch5&dayfrom=' + start_date +'&dayto=' + end_date + '&from=' + str(pagination) )

        except Exception, e:
            print "Error in collecting period: " + repr(e) + ', date: ' + start_date + '...' + end_date + ', from = ' + str(pagination)
            error.write( "Error in collecting period: " + repr(e) + ', date: ' + start_date + '...' + end_date + ', from = ' + str(pagination) + '\n' )
            try:
                driver.quit()
            except Exception, e:
                print repr(e)
            continue

        remove_ad(driver, 'ESM_Tarranurkka')
        remove_ad(driver, 'ESM_Tikkeri')
        remove_ad(driver, 'ESM_avaussivu')

        try:
            element = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'neocontent'))
                )

        except Exception, e:
            print "Error in collecting urls: " + repr(e) + ', date: ' + start_date + '...' + end_date + ', from = ' + str(pagination)
            error.write( "Error in collecting urls: " + repr(e) + ', date: ' + start_date + '...' + end_date + ', from = ' + str(pagination) + '\n' )
            try:
                driver.quit()
            except Exception, e:
                print repr(e)
            continue

        time.sleep(2)

        content = driver.find_element_by_id('neocontent')

        urls = collect_urls(content, start_date, end_date, pagination, error)

        if not urls:
            if check_pagination(content, pagination, error):
                print "Period collected! Finishing..."
                try:
                    driver.quit()
                except Exception, e:
                    print repr(e)
                break

        print "Downloading content: " + start_date + '...' + end_date

        for url in urls:

            s = download( driver, url, raw_dir, error )

            if s == 200:
                downloaded += 1
                print str(downloaded) + " stories downloaded from " + start_date + '...' + end_date

            http_status[ s ] += 1

        pagination += 20

        try:
            driver.quit()
        except Exception, e:
            print repr(e)

    return http_status


def login(driver, username, password, error):
    try:
        print "Logging in..."
        with Timeout(20):
            driver.get('https://media.portal.worldoftulo.com/Login?continue=https%3A%2F%2Fbackend.worldoftulo.com%2Foauth2%2Fauth%3Fclient_id%3D56b9cb80a672017f61000001%26redirect_uri%3Dhttp%253A%252F%252Fwww.ksml.fi%252Ftulo_sso_redirect.jsp%26state%3Dhttp%253A%252F%252Fwww.ksml.fi%252F%2523%26response_type%3Dcode%26oid%3Dmedia%26accountOrigin%3DKE')

        username_elem = driver.find_element_by_id( 'Username' )
        password_elem = driver.find_element_by_id( 'Password' )
        submit_btn = driver.find_element_by_xpath( '//input[@type="submit"]' )

        username_elem.send_keys( username )
        password_elem.send_keys( password )
        submit_btn.click()

    except Exception, e:
        print "Error logging in: " + repr(e)
        error.write("Error logging in: " + repr(e) + '\n' )
        try:
            driver.quit()
        except Exception, e:
            print repr(e)
        return False

    time.sleep(2)
    return True


def remove_ad(driver, ad_id):
    try:
        ad = driver.find_element_by_id( ad_id )
        ad_images = ad.find_elements_by_tag_name('img')
        ad_images[0].click()

    except Exception, e:
        pass


def collect_urls(content, start_date, end_date, pagination, error):
    urls = []

    tags = content.find_elements_by_tag_name('a')

    if not tags:
        error.write( "No urls found: " + start_date + '...' + end_date + ', from = ' + str(pagination) + '\n')
        return urls

    for tag in tags:

        url = get_url_from_element( tag )

        if not url:
            print "Error in getting url: " + start_date + '...' + end_date + ', from = ' + str(pagination)
            error.write( "Error in getting url: " + start_date + '...' + end_date + ', from = ' + str(pagination) + '\n')
            continue

        if 'search' in url:
            continue

        urls.append(url)

    save_urls( urls, start_date, end_date )

    return urls


def get_url_from_element( tag ):
    attempt = 1
    while True:
        try:
            url = tag.get_attribute('href')
        except Exception, e:
            if attempt > 5:
                print "Error in getting url from element: " + repr(e)
                return ''
            attempt += 1
            continue

        break

    return url


def check_pagination(content, pagination, error):
    try:
        paginator = content.find_element_by_class_name('paginatorArchive')
        last_tag = paginator.find_elements_by_tag_name('a')[-1].get_attribute('innerHTML')
    except Exception, e:
        print "Error in checking pagination: " + repr(e) + ', pagination: ' + str(pagination)
        error.write( "Error in checking pagination: " + repr(e) + ', pagination: ' + str(pagination) + '\n')
        return False

    if 'Seuraava' not in last_tag:
        return True
    else:
        return False


def save_urls(urls, start_date, end_date):
    print "Saving urls: " + start_date + '...' + end_date

    url_dir = 'saved_urls/ksml/'

    if not os.path.exists( url_dir ):
        os.makedirs( url_dir )

    try:
        url_log = open( url_dir + start_date + '_' + end_date + '.log', 'w' )

        for url in urls:
            url_log.write( url.replace('neo', 'arkisto/') + '\n' )

    except Exception, e:
        print "Error in saving urls: " + repr(e) + ', date: ' + start_date + '...' + end_date


def download(driver, url, raw_dir, error):
    url = url.replace('neo', 'arkisto/')

    try:
        driver.get(url)

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'neocontent'))
            )

    except Exception, e:
        print "Error in downloading content: " + repr(e) + ', url: ' + url
        error.write( "Error in downloading content: " + repr(e) + ', url: ' + url + '\n')

    finally:

        try:
            content = driver.find_element_by_id('neocontent')

            story = ksml_parser.parse_from_archive( url, content.get_attribute('innerHTML') )

            f = base64.encodestring( url )

            pickle.dump( story, open( raw_dir + f + '.pickle', 'w' ) )

            return story['http']

        except Exception, e:
            print "Error in downloading content: " + repr(e) + ', url: ' + url
            error.write( "Error in downloading content: " + repr(e) + ', url: ' + url + '\n')


def split_to_months(year, inc_months):

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

    if not inc_months:
        return periods

    else:
        months = inc_months.split(',')
        stripped_periods = {}

        for month in months:
            start = month + '01'
            if len(month) == 1:
                start = '0' + start
            stripped_periods[start] = periods[start]

        return stripped_periods


if __name__ == '__main__':

    stamp = datetime.datetime.now().isoformat().split('.')[0]

    raw_dir = 'data-raw/ksml/' + stamp + '/' ## where pickles are stored
    data_dir = 'data/ksml/' + stamp + '/' ## where json outputs are stored
    error_dir = 'error-logs/ksml/' + stamp + '/' ## save error logs here

    for f in [raw_dir, data_dir, error_dir]:
        if not os.path.exists( f ):
            os.makedirs( f )

    display = Display(visible=0, size=(800, 600))
    display.start()

    username = sys.argv[1]
    password = sys.argv[2]

    http_status = collections.defaultdict( int )

    inc_months = sys.argv[3]

    for year in sys.argv[4:]:
        months = split_to_months( year, inc_months )
        print 'Collecting periods: '
        print months

        for start, end in months.items():
            start_date = year + start
            end_date = year + end

            error = open( error_dir + 'error_' + start_date + '_' + end_date + '.log', 'w' )

            http_status = collect_period( start_date, end_date, http_status, error )

    print 'Final status'
    for s, c in http_status.items():
        print s, '\t', c

    # regroup files to nicer folders
    store = downloader.resort_pickles( raw_dir )

    # store files as json
    for filename, data in store.items():
        json.dump( data , open(  data_dir + filename + '.json', 'w' ) )
