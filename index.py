from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# Cria uma instância do navegador
driver = webdriver.Chrome()

# Abre a página do Google
driver.get(
    "https://www.aliseeks.com/search/image?fskey=xApJQY7Gppu84AKK6vX6&site=ali")

sleep(8)

links = []
all_products = driver.find_elements(By.CLASS_NAME, "product-list-item.grid")
for product in all_products:
    link = product.find_element(By.CSS_SELECTOR, ".product-title a")
    href = link.get_attribute("href")
    links.append(href)

for link in links:
    print(link)

for link in links:
    driver.get(link)
    sleep(5)
    price_product = driver.find_elements(By.CLASS_NAME, "_1Hlfk.notranslate")
    print(price_product.text())


driver.close()
