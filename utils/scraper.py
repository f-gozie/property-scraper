from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List


def retrieve_property_urls() -> List[str]:
    """
    Retrieve the urls for all properties on the crexi website
    """
    opt = webdriver.FirefoxOptions()
    opt.add_argument('-headless')
    driver = webdriver.Firefox(options=opt)
    urls = []
    page_number = 25
    url = f'https://www.crexi.com/properties?page={page_number}'

    try:
        while True:
            driver.get(url)

            # Handle load screen delay
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'crx-property-tile-aggregate')))
            urls.extend([element.find_element(By.TAG_NAME, 'a').get_property('href') for element in elements])

            # Move to next page
            page_number += 1
            url = f'https://www.crexi.com/properties?page={page_number}'
    except WebDriverException:
        driver.quit()
        return urls


def retrieve_property_details(property_urls):
    """
    Retrieve details for all properties from the properties urls list
    """
    # for each property in the page, open the property url, and retrieve the required data
    opt = webdriver.FirefoxOptions()
    opt.add_argument('-headless')
    driver = webdriver.Firefox(options=opt)
    data = []
    for url in property_urls:
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

        brokers = driver.find_elements(By.CLASS_NAME, 'brokers-list')
        for broker in brokers:
            broker_name = broker.text.splitlines()[0]
            broker_license = next(license for license in broker.text.splitlines() if "License" in license)

        # add all these data into a dictionary
        prop['property_name'] = property_name.text
        prop['property_description'] = property_description
        prop['property_address'] = property_address.splitlines()[0]
        try:
            prop['property_price'] = property_asking_price
        except NameError:
            prop['property_price'] = property_bidding_price
        prop['broker_name'] = broker_name
        prop['broker_license'] = broker_license

        data.append(prop)

    driver.quit()
    return data


if __name__ == "__main__":
    urls = retrieve_property_urls()
    details = retrieve_property_details(urls)
    print(details)