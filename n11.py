import requests
import pandas as pd
from lxml import html as xhtml
import ast


def get_schema(tree, xpath = "normalize-space(//script[@type = 'application/ld+json'])"):
    schemaDict = ast.literal_eval(tree.xpath(xpath))
    products = schemaDict['mainEntity']['offers']['itemOffered']
    return products

def get_products(tree, xpath = "//div[@class = 'listView']/ul/li"):
    products = tree.xpath(xpath)
    return products


def getProductsInPage(resp, tree):
    productsOfPage = []
    products_schema = get_schema(tree)
    productsTree = get_products(tree)
    

    for product, productJson in zip(productsTree, products_schema):
        temp_dict = {}
        prodName = productJson['name']
        prodUrl = productJson['url']
        prodPrice = float(productJson['offers']['price'].replace(',', ''))
        prodPriceCurrency = productJson['offers']['priceCurrency']
        prodSellerName = productJson['offers']['seller']['name']
        prodSellerType = productJson['offers']['seller']['@type']
        prodImage = productJson['offers']['image']
        try:
            prodRating = float(productJson['aggregateRating']['ratingValue'])
            prodRatingCount = int(productJson['aggregateRating']['reviewCount'])
        except:
            prodRating = None
            prodRatingCount = None
        prodId = product.xpath("normalize-space(div/@id)")
        try:
            position = int(product.xpath("normalize-space(div/@data-position)"))
        except:
            position = None

        try:
            discRate = int(product.xpath("normalize-space(div/div[@class = 'proDetail']\
            /div[@class = 'discount discountS']/div/span[@class = 'ratio'])"))
        except:
            discRate = 0
        branchPointStr = product.xpath("normalize-space(div/a[@class = 'sallerInfo']/div[@class = 'shopPoint']\
            /div/span[@class = 'point'])")
        try:
            branchPoint = int(branchPointStr.replace('%', ''))
        except: 
            branchPoint = None
        badges = str(product.xpath("div/a[@class = 'sallerInfo']/div[@class = 'badgeSaller']/ul/li/span/@class"))


        temp_dict['Name'] = prodName
        temp_dict['Url'] = prodUrl
        temp_dict['Price'] = prodPrice
        temp_dict['Currency'] = prodPriceCurrency
        temp_dict['BranchName'] = prodSellerName
        temp_dict['BranchType'] = prodSellerType
        temp_dict['AvgRating'] = prodRating
        temp_dict['ReviewCount'] = prodRatingCount
        temp_dict['ProductId'] = prodId
        temp_dict['ProductPosition'] = position
        temp_dict['DiscountPercantage'] = discRate
        temp_dict['BranchPoint'] = branchPoint
        temp_dict['BranchBadges'] = badges
        temp_dict['Image'] = prodImage

        productsOfPage.append(temp_dict)
    return productsOfPage


def crawlOverPagination(startUrl):
    url = startUrl
    allProducts = []
    while True:
        nextPageXpath = "normalize-space(//div[@class = 'pagination']/a[@class = 'next navigation']/@href)"
        print(url)
        resp = requests.request('GET', url) 
        tree = xhtml.fromstring(resp.text)
        productsOfPage = getProductsInPage(resp, tree)
        allProducts += productsOfPage
        url = tree.xpath(nextPageXpath)
        if len(url) == 0:
            break
    return allProducts


if __name__ == '__main__':

    allProducts = crawlOverPagination('https://www.n11.com/telefon-ve-aksesuarlari/cep-telefonu')

    df = pd.DataFrame(allProducts)
    writer = pd.ExcelWriter('n11.xlsx')
    df.to_excel(writer, index= False)
    writer.save()
