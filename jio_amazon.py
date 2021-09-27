from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd
import openpyxl as pxl

from time import sleep
import keyboard

from inputs import PINCODE, PATH, products

# OPENING CHROME

# Driver path
chrome_driver_path = PATH

# Setting some options
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# E-commerce website urls
jiomart_url = 'https://www.jiomart.com/'
amazon_fresh_url = 'https://www.amazon.in/alm/storefront?almBrandId=ctnow'

# Open website in chrome
browser = webdriver.Chrome(executable_path = chrome_driver_path, options = options)
browser.get(jiomart_url)
sleep(2)

# Set pincode 
delivery_pincode = browser.find_element_by_id('delivery_details').click()
sleep(0.5)
enter_details = browser.find_element_by_class_name('inp_text').send_keys(PINCODE)
sleep(0.5)
browser.find_element_by_class_name('apply_btn').click()
sleep(2)

# PROCESSING THE DATA

for product in products[:-1]:
    # Search for product
    search_bar = browser.find_element_by_id('search')
    search_bar.send_keys(product)
    sleep(1)
    keyboard.press('enter')
    sleep(5)

    # Check available products
    try:
        instock_checkbox = browser.find_element_by_xpath('//*[@id="in_stock_filter"]/div/ul/li/div/div/div/label').click()
    except: 
        continue
    # Initializing lists to store details about the product
    names = []
    prices = []
    links =[]

    # Access html of the webpage
    content = browser.page_source
    soup = BeautifulSoup(content,'html.parser')

    # Get names, prices & links of the product
    for a in soup.findAll('div', attrs = {'class' : 'cat-item'}):
        name = a.find('span', attrs = {'class' : 'clsgetname'})
        sleep(0.5)
        product_name = [x for x in product.split(' ')]
        for x in product_name:
            if x in str(name.text).lower():
                if name.text not in names:
                    names.append(name.text)

                    price = a.find('span', attrs = {'id' : 'final_price'})
                    prices.append(float(price.text.split(" ")[1]))

                    link = a.find('a', href = True, attrs = {'class' : 'category_name prod-name'})
                    href = link['href']
                    links.append(jiomart_url + href)
    
# Make excel sheet of product

    # Make dataframe of the data collected
    df = pd.DataFrame({'Store name' : 'Jio Mart', 'Product Name':names,'Price':prices,'Links':links})
    df = df.sort_values(by = ['Price'])
    if product == products[0]:
        writer = pd.ExcelWriter('products.xlsx', engine='xlsxwriter')
        writer.save()
        # df.to_excel('products.xlsx', sheet_name = product, index = False, encoding = 'utf-8')

    # Load excel workbook
    excel_book = pxl.load_workbook('products.xlsx')

    with pd.ExcelWriter('products.xlsx', engine='openpyxl') as writer:
        writer.book = excel_book
        writer.sheets = {worksheet.title: worksheet for worksheet in excel_book.worksheets}
        # df.to_excel('products.xlsx', sheet_name = item, index=False, encoding='utf-8')
        df.to_excel(writer, sheet_name = product, index=False, encoding='utf-8') 
        writer.save()
# Jiomart over

# Start amazon fresh
browser.get(amazon_fresh_url)
sleep(2)

# Set pincode
browser.find_element_by_id('glow-ingress-line1').click()
sleep(2)
enter_pincode = browser.find_element_by_id('GLUXZipUpdateInput')
sleep(1)
enter_pincode.send_keys(PINCODE)
sleep(1)
keyboard.press_and_release('enter')
sleep(2)

for product in products[:-1]:
    # Search bar
    search_bar = browser.find_element_by_id('twotabsearchtextbox')
    sleep(1)
    search_bar.click()
    sleep(0.5)
    keyboard.send("ctrl+a")
    sleep(0.5)
    keyboard.press_and_release('delete')
    sleep(0.5)
    search_bar.send_keys(product + ' in fresh')
    sleep(1)
    keyboard.press_and_release('enter')
    sleep(2)

    # Initializing lists to store details about the product
    names = []
    prices = []
    links =[]

    # Access html of the webpage
    content = browser.page_source
    soup = BeautifulSoup(content,'html.parser')

    # Get names, prices & links of the product
    for a in soup.findAll('div', attrs = {'class' : 'a-section a-spacing-medium'}):
        name = a.find('span', attrs = {'class' : 'a-size-base-plus a-color-base a-text-normal'})
        try: 
            test= str(name.text)
        except: 
            continue
        product_name = [x for x in product.split(' ')]
        for x in product_name:
            if x  in str(name.text).lower():
                if name.text not in names:
                    names.append(name.text)

                    price = a.find('span', attrs = {'class' : 'a-price-whole'})
                    try:
                        prices.append(float(price.text))
                    except ValueError:
                        price = price.text.replace(',','')
                        prices.append(float(price))
                    link = a.find('a', href = True, attrs = {'class' : 'a-link-normal a-text-normal'})
                    href = link['href']
                    links.append('https://www.amazon.in/' + href)

# Make excel sheet of product

    # Make dataframe of the data collected
    df = pd.DataFrame({'Store name' : 'Amazon Fresh', 'Product Name':names,'Price':prices,'Links':links})
    df = df.sort_values(by = ['Price'])

    # Load excel workbook
    excel_book = pxl.load_workbook('products.xlsx')

    with pd.ExcelWriter('products.xlsx', engine='openpyxl') as writer:
        writer.book = excel_book
        writer.sheets = {worksheet.title: worksheet for worksheet in excel_book.worksheets}
        # df.to_excel('products.xlsx', sheet_name = item, index=False, encoding='utf-8')
        df.to_excel(writer, sheet_name = product, startcol = 5, index=False, encoding='utf-8') 
        writer.save()


browser.quit()