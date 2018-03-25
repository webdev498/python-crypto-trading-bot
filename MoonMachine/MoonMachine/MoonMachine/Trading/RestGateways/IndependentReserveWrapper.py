from MoonMachine.Trading.RestGateways.IExchangeWrapper import IExchangeWrapper
from MoonMachine.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries
from pyalgotrade.bar import BasicBar, Frequency, Bar
from ccxt.independentreserve import independentreserve

from ccxt.bittrex import bittrex

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
        self.__base = bittrex()
        self.__name = self.__base.describe()['name'].lower()
        self.__log = getLogger(str(self.__class__))
        self.__profitPercentage = Decimal('0.02')


    @overrides
    def Name(self):
        return self.__name

    @overrides
    def AttemptAuthentication (self, authDetails = dict):
        try:            
            self.__base.apiKey = authDetails[self.__name]['apiKey']
            self.__base.secret = authDetails[self.__name]['secret']

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.Name() + ". " + str(e)
            self.__log.error(error)
            return error

        try:
            self.__base.fetch_balance()
            return ''

        except Exception as e:
            error = 'authentication failed using given apiKey and secret for exchange: ' + self.__name + ". " + str(e)
            self.__log.error(error)
            return error

    @overrides
    def GetMarketUpdate(self, lastKnownBar = Bar, labels = list, pairsSymbol = str):
        """Returns a LabeledBar of todays market summary."""
        
        #response = requests.get (requestLocator)
        #jsonResult = response.json()
        #dateBarCreated = jsonResult['CreatedTimestampUtc']
        #DayHighestPrice = jsonResult['DayHighestPrice']
        #DayLowestPrice = jsonResult['DayLowestPrice']
        #DayVolumeXbt = jsonResult['DayVolumeXbt']
        #LastPrice = jsonResult['LastPrice']

        #dateBarCreated = datetime.utcfromtimestamp(dateBarCreated)

        #rawSummary = BasicBar(dateBarCreated,
        #                        lastKnownBar.getClose(),
        #                        DayHighestPrice,
        #                        DayLowestPrice,
        #                        LastPrice,
        #                        DayVolumeXbt,
        #                        LastPrice,
        #                        0,
        #                        None)

        #labeledSeries = LabeledBarSeries([labeledSummary], labels)
        #return labeledSeries

    @overrides
    def Buy(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def Sell(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def ExchangesMinimumProfitPercentage(self):
        self.__log.info("returning a profit percentage of " + str(self.__profitPercentage))
        return self.__profitPercentage

    @overrides
    def GetOpenOrders(self, pairsSymbol = str):
        pairsSymbol = 'BTC/USDT'
        self.__base.load_markets()
        market = self.__base.market(pairsSymbol)
        request = dict()
        request['market'] = market['id']

        try:
            response = self.__base.marketGetOpenorders(request)
            orders = self.__base.parse_orders(response['result'], market)
            filteredOrders = self.__base.filter_by_symbol(orders, pairsSymbol)
            #return map()

        except Exception as e:
            self.__log.error(self.__name + " context does not have api method marketGetOpenorders. " + str(e))
            raise

    @overrides
    def CancelOrder(self, order = Order):
        self.__base.cancel_order()

    @overrides
    def ExchangesRateLimit(self):
        return NotImplementedError()