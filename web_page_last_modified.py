import csv
import requests
import lxml.html
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from htmldate import find_date

options=webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver=webdriver.Chrome(chrome_options=options)
try:
    with open('dataset_op.csv', 'a') as wf:
        writer=csv.writer(wf)
        writer.writerow(['text', 'url', 'status_code', 'header_modified', 'modified_text_if_any', 'Percentage', 'SEO', 'Content', 'meta_data'])
        with open('dataset.csv', 'r') as f:
            reader=csv.reader(f, delimiter=',')
            for row in reader:
                data=requests.get(row[1])
                try:
                    published_date=find_date(row[1])
                except:
                    published_date='date not found'
                data_text=lxml.html.fromstring(data.content)
                soup1 = BeautifulSoup(data.content, 'html.parser')
                dict1={}
                try:
                    for sp in soup1.find_all('meta'):
                        property = sp.get('property')
                        content = sp.get('content')
                        if property == None:
                            property=sp.get('name')
                            dict1[property] = content
                        dict1[property]=content
                        if None in dict1:
                            del dict1[None]
                        else:
                            pass
                except:
                    print('no meta tag found')
                driver.get('https://en.ryte.com/website-checker/')
                driver.find_element_by_xpath('//input[@name="website"]').send_keys(
                    row[1])
                time.sleep(2)
                # driver.find_element_by_xpath('//input[@type="submit"]').click()
                WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, '//input[@type="submit"]'))).click()
                WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@class="metric total_score"]')))
                data1 = driver.page_source
                soup = BeautifulSoup(data1, 'html.parser')
                percentage = soup.find('div', {"class": "metric total_score"}).get('data-ratio')
                seo = soup.find('a', {"href": "#seo"}).find_parent().find('p').text
                content = soup.find('a', {"href": "#content"}).find_parent().find('p').text
                writer.writerow([row[0], row[1], data.status_code, data.headers.get('last-modified', ''), published_date, percentage, seo, content, dict1])
                print(row[0], row[1], data.status_code, data.headers.get('last-modified', ''), '')
except Exception as e:
    print(e, row[1])
