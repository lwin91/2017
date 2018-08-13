# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time
import os, json
from random import uniform
from selenium.webdriver.chrome.options import Options

MAIN_URL = 'https://www.linkedin.com/uas/login?session_redirect=%2Fvoyager%2FloginRedirect%2Ehtml&fromSignIn=true&trk=uno-reg-join-sign-in'

PROXY = "35.185.201.225:8080"

options = Options()
options.add_argument('--blink-settings=imagesEnabled=false')
# uncomment below line to enable proxy
# options.add_argument('--proxy-server=%s' % PROXY) 
driver = webdriver.Chrome('chromedriver', chrome_options=options)
driver.maximize_window()
driver.get('https://www.linkedin.com')
l = driver.find_element_by_xpath('//label[@class="lang-selector-state-label"]')
l.click()
driver.find_element_by_xpath('//button[text()="English"]').click()

time.sleep(5)
driver.get(MAIN_URL)
rus = driver.find_element_by_xpath('//div[@class="forgot-password-container"]/a').text
while True:
	if rus == 'Forgot password?':
		break
	else:
		driver.get('https://www.linkedin.com')
		l = driver.find_element_by_xpath('//label[@class="lang-selector-state-label"]')
		l.click()
		driver.find_element_by_xpath('//button[text()="English"]').click()
		time.sleep(5)
		driver.get(MAIN_URL)
		rus = driver.find_element_by_xpath('//div[@class="forgot-password-container"]/a').text
login = driver.find_element_by_xpath('//input[@name="session_key"]')
login.send_keys('test@gmail.com')
password = driver.find_element_by_xpath('//input[@name="session_password"]')
password.send_keys('123456789')
password.submit()
time.sleep(3)


a = csv.DictReader(open('6.csv', encoding='utf-8'))
for num, row in enumerate(a, 1):
	# url = row['Url']
	url = 'https://www.linkedin.com/company/{}'.format(row['company_id'])
# j = json.loads(a)
# for num, row in enumerate(j['ids'], 1):
# 	url = 'https://www.linkedin.com/company/{}'.format(row)

	if url.lower() == 'url':
		continue
	try:
		driver.get(url)
	except:
		url = 'https://' + row['Url']
		driver.get(url)
	
	if 'Page not found' in driver.page_source:
		print('This profile is not available')
		data = {'Url': url}
		with open('empty.csv', 'a', encoding='utf-8', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=data.keys())
			if not os.fstat(f.fileno()).st_size:
				writer.writeheader()
			writer.writerow(data)
		continue
	try:
		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h1[@class="top-card__title"]')))
	except:
		print('Error')
		driver.close()
		time.sleep(30)
		driver = webdriver.Chrome('chromedriver', chrome_options=options)
		driver.maximize_window()
		driver.get('https://www.linkedin.com')
		l = driver.find_element_by_xpath('//label[@class="lang-selector-state-label"]')
		l.click()
		driver.find_element_by_xpath('//button[text()="English"]').click()

		time.sleep(10)
		driver.get(MAIN_URL)

		rus = driver.find_element_by_xpath('//div[@class="forgot-password-container"]/a').text
		while True:
			if rus == 'Forgot password?':
				break
			else:
				driver.get('https://www.linkedin.com')
				l = driver.find_element_by_xpath('//label[@class="lang-selector-state-label"]')
				l.click()
				driver.find_element_by_xpath('//button[text()="English"]').click()
				time.sleep(5)
				driver.get(MAIN_URL)
				rus = driver.find_element_by_xpath('//div[@class="forgot-password-container"]/a').text
		login = driver.find_element_by_xpath('//input[@name="session_key"]')
		login.send_keys('test@gmail.com')
		password = driver.find_element_by_xpath('//input[@name="session_password"]')
		password.send_keys('123456789')
		password.submit()
		time.sleep(3)
		continue
	company_id = url.split('/')[-1]
	company_name = driver.find_element_by_xpath('//h1[@class="top-card__title"]').text
	print(num, company_name)
	if len(driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')) == 1:
		if 'follower' in driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')[0].text:
			followers = driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')[0].text.split()[0]
		else:
			break
	else:
		try:
			sector = driver.find_element_by_xpath('//span[@class="top-card__information-text"]').text
		except:
			sector = ''
		try:
			location = driver.find_element_by_xpath('//span[@itemprop="address"]').text
		except:
			location = ''
		try:
			followers = driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')[2].text.split()[0]
		except IndexError:
			if 'follower' in driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')[1].text:
				followers = driver.find_elements_by_xpath('//span[@class="top-card__information-text"]')[1].text.split()[0]
			else:
				break
	try:
		number_of_employees = [i.text for i in driver.find_elements_by_xpath('//a[contains(@class,"top-card__employees-link")]')]
	except:
		number_of_employees = ''
	try:
		see_more = driver.find_element_by_xpath('//label[@data-tracking-control-name="about_showMore"]')
		see_more.click()
		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h3[text()="Size"]')))
	except:
		pass
	try:
		website = driver.find_element_by_xpath('//h3[text()="Website"]/following-sibling::p/a').text
	except:
		website = ''
	try:
		headquarters = driver.find_element_by_xpath('//h3[text()="Headquarters"]/following-sibling::p').text
	except:
		headquarters = ''
	try:
		year_founded = driver.find_element_by_xpath('//h3[text()="Year Founded"]/following-sibling::p').text
	except:
		year_founded = ''
	try:
		company_type = driver.find_element_by_xpath('//h3[text()="Company Type"]/following-sibling::p').text
	except:
		company_type = ''
	# try:
	# 	company_size = driver.find_element_by_xpath('//p[contains(@class,"company-module__company-staff-count")]').text
	# except:
	# 	company_size = ''
	data = {'Company ID': company_id, 'Company Name': company_name, 'Sector': sector,
			'Location': location, 'Followers': followers, 'Number of employees on linkedin': number_of_employees,
			'Website': website, 'Headquarters': headquarters, 'Year Founded': year_founded,
			'Company Type': company_type}
	with open('6_output.csv', 'a', encoding='utf-8', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=data.keys())
		if not os.fstat(f.fileno()).st_size:
			writer.writeheader()
		writer.writerow(data)
