from MoonMachine.Trading.RestGateways.IExchangeWrapper import IExchangeWrapper
from MoonMachine.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries
from pyalgotrade.bar import BasicBar, Frequency
from ccxt.independentreserve import independentreserve

from overrides import overrides
import json
from datetime import datetime
from logging import getLogger, Logger
from decimal import Decimal

class IndependentReserveWrapper(IExchangeWrapper):
    """description of class"""

    def __init__(self):
        super().__init__()
        
        self.__apiKey = str()
        self.__apiSecret = str()
        self.__base = independentreserve()
        self.__name = self.__base.describe()['name']
        self.__log = getLogger(str(self.__class__))
        self.__profitPercentage = Decimal('0.02')


    @overrides
    def Name(self):
        return self.__name

    @overrides
    def AttemptAuthentication (self, authDetails = dict):
        try:            
            self.__base.apiKey = authDetails['independent reserve']['apiKey']
            self.__base.secret = authDetails['independent reserve']['secret']

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.Name() + ". " + str(e)
            self.__log.error(error)
            return error

        try:
            self.__base.fetch_balance()

            return ''

        except Exception as e:
            error = 'authentication failed using given apiKey and secret for exchange: ' + self.__name + ". " + str(e)
            self.__log(error)
            return error

    @overrides
    def GetMarketUpdate(self, lastKnownBar = BasicBar, labels = list, primarySecurity = str, secondarySecurity = str):
        """Returns a LabeledBar of todays market summary."""
        requestLocator = r"https://api.independentreserve.com/Public/GetMarketSummary?primarycurrencycode=" + primarySecurity + "&secondarycurrencycode=" + secondarySecurity
        response = requests.get (requestLocator)
        jsonResult = response.json()
        dateBarCreated = jsonResult['CreatedTimestampUtc']
        DayHighestPrice = jsonResult['DayHighestPrice']
        DayLowestPrice = jsonResult['DayLowestPrice']
        DayVolumeXbt = jsonResult['DayVolumeXbt']
        LastPrice = jsonResult['LastPrice']

        dateBarCreated = datetime.utcfromtimestamp(dateBarCreated)

        rawSummary = BasicBar(dateBarCreated,
                                lastKnownBar.getClose(),
                                DayHighestPrice,
                                DayLowestPrice,
                                LastPrice,
                                DayVolumeXbt,
                                LastPrice,
                                0,
                                None)

        labeledSeries = LabeledBarSeries([labeledSummary], labels)
        return labeledSeries

    @overrides
    def Buy(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def Sell(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def ExchangesMinimumProfitPercentage(self):
        self.__log.info("returning a profit percentage of " + str(self.__profitPercentage))
        return self.__profitPercentage

    @overrides
    def GetOpenOrders(self, primarySecurity = str, secondarySecurity = str):
        stuff = self.__base.fetch_order_book(symbol = secondarySecurity + "/" + primarySecurity)
        symbols = self.__base.symbols
        pass
        #try:
        #    orders = self.__base.fetch_open_orders(symbol = secondarySecurity + "/" + primarySecurity)
        #    return orders

        #except Exception as e:
        #    self.__log.error(self.__base.name + " context could not use api method fetch_open_orders. " + str(e))
        #    raise

#        self.load_markets()
#        request = {}
#        market = None
#        if symbol:
#            market = self.market(symbol)
#            request['market'] = market['id']
#        response = self.marketGetOpenorders(self.extend(request, params))
#        orders = self.parse_orders(response['result'], market, since, limit)
#return self.filter_by_symbol(orders, symbol)

    @overrides
    def CancelOrder(self, order = Order):
        return Transaction() 

    @overrides
    def ExchangesRateLimit(self):
        return NotImplementedError()