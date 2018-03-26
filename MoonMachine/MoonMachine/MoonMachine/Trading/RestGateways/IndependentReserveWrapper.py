from MoonMachine.Trading.RestGateways.IExchangeWrapper import IExchangeWrapper
from MoonMachine.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries
from pyalgotrade.bar import BasicBar, Frequency, Bar
from ccxt.independentreserve import independentreserve
from overrides import overrides
import json
from datetime import datetime
from logging import getLogger, Logger
from decimal import Decimal
from MoonMachine.SelectionOptions.MarketAction import MarketAction

class IndependentReserveWrapper(IExchangeWrapper):
    """description of class"""
    PRIMARY_CURRENCY_LABEL = 'primaryCurrencyCode' #fixed bug where labels are lowercase
    SECONDARY_CURRENCY_LABEL = 'secondaryCurrencyCode'
    VALUE_LABEL = 'Value'
    VOLUME_LABEL = 'Volume'

    def __init__(self):
        super().__init__()
        
        self.__apiKey = str()
        self.__apiSecret = str()
        self.__base = independentreserve()
        self.__base.load_markets()
        self.__name = self.__base.describe()['name'].lower()
        self.__log = getLogger(str(self.__class__))
        self.__profitPercentage = Decimal('0.02')


    @overrides
    def Name(self):
        return self.__name

    @overrides
    def AttemptAuthentication (self, authDetails = dict):
        try:            
            self.__base.apiKey = authDetails[self.Name()]['apiKey']
            self.__base.secret = authDetails[self.Name()]['secret']

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.Name() + ". " + str(e)
            self.__log.error(error)
            return error

        try:
            self.__base.fetch_balance()
            return ''

        except Exception as e:
            error = 'authentication failed using given apiKey and secret for exchange: ' + self.Name() + ". " + str(e)
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
    def GetOpenOrders(self, primarySecurity = str, secondarySecurity = str, pageIndex = 1, pageSize = 50):
        response = self._BubbleWrapRequest(self.__base.privatePostGetOpenOrders, {
            IndependentReserveWrapper.PRIMARY_CURRENCY_LABEL  : secondarySecurity,
            IndependentReserveWrapper.SECONDARY_CURRENCY_LABEL : primarySecurity,
            'pageIndex': str(pageIndex),
            'pageSize': str(pageSize)
        })
        return map(self._ConvertJsonToOrder, response['Data'])


    @overrides
    def CancelOrder(self, order = Order):
        self._BubbleWrapRequest(self.__base.cancel_order, order.GetCloudOrderId())

    @overrides
    def ExchangesRateLimit(self):
        pass

    @overrides
    def _ConvertJsonToOrder(self, jsonObject = dict):
        marketAction = None
        currentReceivedAount = None
        currentGivenAmount = None
        currentSymbol = str.capitalize(jsonObject[IndependentReserveWrapper.PRIMARY_CURRENCY_LABEL] + '/' + jsonObject[IndependentReserveWrapper.SECONDARY_CURRENCY_LABEL])

        if jsonObject['OrderType'] == 'LimitOffer':
            marketAction = MarketAction.BUY
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VALUE_LABEL]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VOLUME_LABEL]

        else:
            marketAction = MarketAction.SELL
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VOLUME_LABEL]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VALUE_LABEL]

        return Order(jsonObject['OrderGuid'], #fixed bug where order guid's label is pascal case
                     self.Name(),
                     marketaction,
                     currentSymbol,
                     currentReceivedAmount,
                     currentGivenAmount,
                     jsonObject['CreatedTimestampUtc'])