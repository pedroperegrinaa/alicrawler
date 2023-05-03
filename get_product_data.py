from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re


def getProductData(shippings_products, prices_products, link,
                   qtd_reviews, qtd_orders, star_rating):
    nova_janela = webdriver.Chrome()

    print(link)

    nova_janela.get(link)

    sleep(2)

    getPrices(nova_janela, shippings_products, prices_products)
    getQtdOrdersAndReviews(nova_janela, qtd_reviews, qtd_orders, star_rating)
    # getReviewAndRating(nova_janela)

    nova_janela.quit()


def getReviewAndRating(nova_janela):
    sleep(2)

    nova_janela.execute_script("window.scrollBy(0, 1000)")
    sleep(2)

    open_reviews = WebDriverWait(nova_janela, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="product-detail"]/div[2]/div/div[1]/ul/li[2]'))
    )
    open_reviews.click()
    sleep(2)

    br_reviews = WebDriverWait(nova_janela, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="cb-onlyFromMyCountry-filter"]'))
    )
    br_reviews.click()

    sleep(1)

    stars = nova_janela.find_elements(
        By.XPATH,
        '//*[@id="transction-feedback"]/div[5]/div[1]/div[2]/div[1]/span/span')

    comments = nova_janela.find_elements(
        By.XPATH,
        '//*[@id="transction-feedback"]/div[5]/div[1]/div[2]/div[3]/dl/dt/span[1]'
    )

# Acesse o valor da propriedade "width" de cada um dos spans encontrados
    for star in stars:
        width = star.getCssValue('width')
        print(f'O valor de width do star é {width}')

    for comment in comments:
        text = comment.getText()
        print(f'O valor de text de comment é {text}')


def getQtdOrdersAndReviews(nova_janela, qtd_reviews, qtd_orders, star_rating):

    getOne_qtd_reviews = "0"
    try:
        getOne_qtd_reviews = nova_janela.find_element(
            By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "black-link", " " ))]')
        print(getOne_qtd_reviews.text)
        qtd_reviews.append(re.sub(r"[^0-9.]", "", getOne_qtd_reviews.text))
    except:
        print('quantidade de reviews nao encontrada')
        qtd_reviews.append(getOne_qtd_reviews)

    getOne_qtd_orders = "0"
    try:
        getOne_qtd_orders = nova_janela.find_element(
            By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "product-reviewer-sold", " " ))]')
        print(getOne_qtd_orders.text)
        qtd_orders.append(re.sub(r"[^0-9.]", "", getOne_qtd_orders.text))
    except:
        print('quantidade de orders nao encontrada')
        qtd_orders.append(getOne_qtd_orders)

    getOne_star_rating = "0"
    try:
        getOne_star_rating = nova_janela.find_element(
            By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "overview-rating-average", " " ))]')
        print(getOne_star_rating.text)
        star_rating.append(getOne_star_rating.text)
    except:
        print('quantidade de stars nao encontrada')
        star_rating.append(getOne_star_rating)

    print(qtd_reviews)
    print(qtd_orders)
    print(star_rating)


def getPrices(nova_janela, shippings_products, prices_products):
    # coleta o valor do frete

    shipping_product = "0.0"

    try:
        shipping_product = nova_janela.find_element(
            By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "dynamic-shipping-titleLayout", " " ))]//strong')
        print(shipping_product.text)
        shippings_products.append(
            re.sub(r"[^0-9.]", "", shipping_product.text))
    except:
        print('preço do frete não encontrado')
        shippings_products.append(shipping_product)

    price_product = "0.0"

    try:
        # coleta o valor do produto com preço em vermelho
        print("preço vermelho")

        price_product = nova_janela.find_element(
            By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "uniform-banner-box-price", " " ))]')
        print("Preço do produto: " + price_product.text)
        prices_products.append(re.sub(r"[^0-9.]", "", price_product.text))

    except NoSuchElementException:
        print("Preço vermelho nao encontrado")
        prices_products.append(price_product)

    try:
        # coleta o valor do produto com prço em branco
        print("preço branco")

        if nova_janela.find_elements(
                By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "_1Hlfk", " " ))]/*'):
            price_product = nova_janela.find_elements(
                By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "_1Hlfk", " " ))]/*')
            price_text = ''.join([elem.text for elem in price_product])
            print("Preço do produto: " + price_text)
            prices_products.append(re.sub(r"[^0-9.]", "", price_text))

    except NoSuchElementException:
        print("Preço branco nao encontrado")

    print("Preço do produto: ")
    print(prices_products)
    print("Frete: ")
    print(shippings_products)
