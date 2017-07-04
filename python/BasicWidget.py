import requests
from lxml import html

import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton

class PriceLookup():
    def __init__(self):
        self.priceURL = "http://2007.runescape.wikia.com/wiki/Exchange:"
        self.suggestionURL = "http://2007.runescape.wikia.com/wiki/"
        self.suggestions = {}


    def getSuggestionMessge(self,key):
        return "not found... Did you mean " + self.suggestions[key]

    def buildTree(self, URL):
        page = requests.get(URL)
        return html.fromstring(page.content)


    def getGEPrice(self, raw_item):
        item = raw_item.replace(" ", "_").capitalize()

        URL = self.priceURL + item

        tree = self.buildTree(URL)

        prices = tree.xpath('//*[@id="GEPrice"]/text()')

        if len(prices) == 0:
            URL = self.suggestionURL + item
            tree = self.buildTree(URL)

            suggestion = tree.xpath('//*[@id="mw-content-text"]/div/h3//text()')
            self.suggestions[raw_item] = suggestion[2]
            return -1

        return prices[0]


class PriceGuide(BaseWidget):

    def __init__(self):
        super(PriceGuide,self).__init__('OSRS Price Guide')

        #Definition of the forms fields
        self._itemname     = ControlText('Item Name', 'Iron Arrow')
        self._price        = ControlText('Item Price')
        self._button        = ControlButton('Look up Price')

        #Define the button action
        self._button.value = self.__buttonAction

        self._formset = [('_itemname', '_button'), '_price', ' ']
        self.price_finder = PriceLookup()

    def __buttonAction(self):
        """Button action event"""
        price = self.price_finder.getGEPrice(self._itemname.value)
        if price < 0:
            self._price.value = self.price_finder.getSuggestionMessge(self._itemname.value)
        else:
            self._price.value = price

#Execute the application
if __name__ == "__main__":   pyforms.startApp( PriceGuide )