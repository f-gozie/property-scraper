import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.crexi.com/properties?page=24'
opt = webdriver.FirefoxOptions()
opt.add_argument('-headless')
driver = webdriver.Firefox(options=opt)
next_page = True

while next_page:
	print(url)
	driver.get(url)
	# next_url = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'next')))
	next_url = driver.find_elements(By.CLASS_NAME, 'next')
	if len(next_url) > 0:

		url = next_url[0].find_element(By.TAG_NAME, 'a').get_property('href')
	else:
		next_page = False
		print("Done")

driver.quit()