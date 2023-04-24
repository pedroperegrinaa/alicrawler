from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from get_product_data import getProductData
import sys
import json

if len(sys.argv) < 2 or len(sys.argv[1]) == 0:
    link_do_produto = "https://www.aliseeks.com/search/image?fskey=qqgOwJKJKqHD4mVrlpGD&site=ali"
else:
    link_do_produto = sys.argv[1]

print("O produto é: ", link_do_produto)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get(link_do_produto)

sleep(3)

links = driver.find_elements(
    By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "line-limit", " " ))]//a')

products = []
for link in links:
    href = link.get_attribute('href')
    data = {
        "link-product": href,
        "price-product": "",
        "price-shipping": ""
    }
    products.append(data)

prices_products = []
shippings_products = []

qtd_reviews = []
qtd_orders = []
star_rating = []

for product in products:
    link = product["link-product"]

    getProductData(shippings_products, prices_products, link,
                   qtd_reviews, qtd_orders, star_rating)


for i, data in enumerate(products):
    data["price-product"] = prices_products[i]["price-product"]
    data["price-shipping"] = shippings_products[i]["price-shipping"]

driver.close()
