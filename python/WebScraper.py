import pyforms
import sys
import os
from lxml import html
import requests


def getGEPrice(item):
    subURL = "http://2007.runescape.wikia.com/wiki/Exchange:"
    URL = subURL + item

    page = requests.get(URL)
    tree = html.fromstring(page.content)
    prices = tree.xpath('//*[@id="GEPrice"]/text()')
    if len(prices) == 0:
        suggestion = tree.xpath('//*[@id="mw-content-text"]/div/h3/text()')
        print item," not found.\n\tDid you mean: ",suggestion
        return -1
    return prices[0]


args = sys.argv
items = args[1:]
for item in items:
    item = item.capitalize()
    item = item.replace(" ", "_")
    price = getGEPrice(item)
    if price >= 0 :
        print item," Price: ",price

