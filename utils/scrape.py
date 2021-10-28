import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def retrieve_properties():
	url = 'https://www.crexi.com/properties'
	opt = webdriver.FirefoxOptions()
	opt.add_argument('-headless')
	driver = webdriver.Firefox(options=opt)
	next_page = True
	data = []

	while next_page:
		driver.get(url)
		print(url)

		# get url for next page
		next_url = driver.find_elements(By.CLASS_NAME, 'next')

		# get all elements matching the XPATH, then get their href values
		elements = driver.find_elements(By.XPATH, '//crx-property-tile-aggregate')
		url_list = [ element.find_element(By.TAG_NAME, 'a').get_property('href') for element in elements ]

		# for each property in the page, open the property url, and retrieve the required data
		for url in url_list:
			prop = {}
			driver.get(url)
			property_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'property-name')))
			property_description = driver.find_element(By.CLASS_NAME, 'property-description').text
			property_address = driver.find_element(By.CLASS_NAME, 'address-line').text

			# some properties only have bidding prices and no asking prices. so consider that
			try:
				property_asking_price = driver.find_element(By.XPATH, '//crx-pdp-terms/div[2]/div[1]/span[2]/span').text
			except NoSuchElementException:
				property_bidding_price = driver.find_element(By.CLASS_NAME, 'term-value').text
			broker_name = driver.find_element(By.CLASS_NAME, 'name').text
			broker_license = driver.find_element(By.XPATH, '//crx-pdp-broker-cards/div/ul/li/div/div[3]').text

			# add all these data into a dictionary
			prop['property_name'] = property_name.text
			prop['property_description'] = property_description
			prop['property_address'] = property_address.splitlines()[0]
			try:
				prop['property_price'] = property_asking_price
			except NameError:
				prop['property_price'] = property_bidding_price
			prop['broker_name'] = broker_name.split('PRO')[0].splitlines()[0]
			prop['broker_license'] = broker_license

			# print(prop)
			data.append(prop)
			# print(data)

		# If len(next_url) is less than 0, it means there's no next page element. So the loop can end here
		if len(next_url) > 0:
			url = next_url[0].find_element(By.TAG_NAME, 'a').get_property('href')
		else:
			next_page = False

	driver.quit()
	# with open('result.json', 'w') as fp:
	# 	json.dump(data, fp)
	return data

print(retrieve_properties())
