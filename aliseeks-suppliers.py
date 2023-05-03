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

links_bruto = driver.find_elements(
    By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "line-limit", " " ))]//a')

links = []
products = []
for link_bruto in links_bruto:
    href = link_bruto.get_attribute('href')
    links.append(href)

print(links)

prices_products = []
shippings_products = []

qtd_reviews = []
qtd_orders = []
star_rating = []

total_array = []


for link in links:

    getProductData(shippings_products, prices_products, link,
                   qtd_reviews, qtd_orders, star_rating)


if len(prices_products) != len(shippings_products):
    print("Os arrays têm comprimentos diferentes.")
else:

    for i in range(len(prices_products)):
        if not prices_products[i]:
            prices_products[i] = '0'
        if not shippings_products[i]:
            shippings_products[i] = '0'

        total = float(prices_products[i]) + float(shippings_products[i])

        total_array.append(total)

    print("O novo array com as totals é:", total_array)

combined = list(zip(links, prices_products, shippings_products, total_array,
                qtd_reviews, qtd_orders, star_rating))

data = {"data": []}

for values in combined:
    data["data"].append({"link": values[0], "preco": values[1], "frete": values[2], "total": values[3],
                        "qtd-reviews": values[4], "qtd-pedidos": values[5], "estrelas": values[6]})


open("products.json", "w").close()

with open("products.json", "w") as file:
    json.dump(data, file)

# with open("products.json") as f:
#     data = json.load(f)

# sorted_data = sorted(data["data"], key=lambda x: (-int(x["qtd-reviews"]
#                                                        ), -float(x["estrelas"]), float(x["total"])))

# with open("products_sorted.json", "w") as f:
#     json.dump({"data": sorted_data}, f, indent=4)

# print(sorted_data)


driver.close()
