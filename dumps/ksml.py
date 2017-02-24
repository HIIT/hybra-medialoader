import time
import json
import ksml

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download(year, username, password):
    driver = webdriver.Firefox()

    login(driver, username, password)

    urls = collect_urls(driver, year)

    collect_content(driver, urls)

    driver.quit()


def login(driver, username, password):
    driver.get('https://media.portal.worldoftulo.com/Login?continue=https%3A%2F%2Fbackend.worldoftulo.com%2Foauth2%2Fauth%3Fclient_id%3D56b9cb80a672017f61000001%26redirect_uri%3Dhttp%253A%252F%252Fwww.ksml.fi%252Ftulo_sso_redirect.jsp%26state%3Dhttp%253A%252F%252Fwww.ksml.fi%252F%2523%26response_type%3Dcode%26oid%3Dmedia%26accountOrigin%3DKE')

    username_elem = driver.find_element_by_id('Username')
    password_elem = driver.find_element_by_id('Password')
    submit_btn = driver.find_element_by_xpath('//input[@type="submit"]')

    username_elem.send_keys(username)
    password_elem.send_keys(password)
    submit_btn.click()

    time.sleep(10)


def collect_urls(driver, year):
    driver.get('http://www.ksml.fi/arkisto/?tem=archive_lsearch5&dayfrom=19960101&dayto=19960102')

    urls = []

    while True:
        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, 'neocontent'))
                )
        finally:
            remove_ad(driver)

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

    return urls


def save_urls(urls):
    pass


def collect_content(driver, urls):
    i = 1
    for url in urls:
        driver.get(url.replace('neo', 'arkisto/'))
        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, 'neocontent'))
                )
        finally:
            content = driver.find_element_by_id('neocontent')
            data = ksml.parse_from_archive( url, content.get_attribute('innerHTML') )
            json.dump( data , open(  'ksml_test/' + str(i) + '.json', 'w' ) )
            i += 1


def remove_ad(driver):
    try:
        ad = driver.find_element_by_id('ESM_Tarranurkka')
        ad_images = ad.find_elements_by_tag_name('img')
        ad_images[0].click()
    except Exception, e:
        pass
