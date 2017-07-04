import sys
from lxml import html
import requests

priceURL = "http://2007.runescape.wikia.com/wiki/Exchange:"
suggestionURL = "http://2007.runescape.wikia.com/wiki/"

args = sys.argv
items = args[1:]

suggestions = {}


def printSuggestions():
    print
    for bad, good in suggestions.items():
        print bad, "not found... Did you mean", good
    return


def buildTree(URL):
    page = requests.get(URL)
    return html.fromstring(page.content)


def getGEPrice(raw_item):

    item = raw_item.replace(" ", "_").capitalize()

    URL = priceURL + item

    tree = buildTree(URL)

    prices = tree.xpath('//*[@id="GEPrice"]/text()')

    if len(prices) == 0:
        URL = suggestionURL + item
        tree = buildTree(URL)

        suggestion = tree.xpath('//*[@id="mw-content-text"]/div/h3//text()')
        suggestions[raw_item] = suggestion[2]
        return -1

    return prices[0]


print "Item\t\t\t|Price (gp)"
print "------------------------+-----------"
for aitem in items:
    price = getGEPrice(aitem)
    if price >= 0 :
        if len(aitem) < 16:
            aitem = aitem + "\t"
        print aitem, "\t|", price
printSuggestions()
