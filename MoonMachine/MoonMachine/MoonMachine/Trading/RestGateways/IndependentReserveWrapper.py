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

from django.contrib.auth import get_user

class IndependentReserveWrapper(IExchangeWrapper):
    """description of class"""
    PRIMARY_CURRENCY = 'primaryCurrencyCode' #fixed bug where labels are lowercase
    SECONDARY_CURRENCY = 'secondaryCurrencyCode'
    VALUE = 'Value'
    VOLUME = 'Volume'
    PAGE_INDEX = 'pageIndex'
    PAGE_SIZE = 'pageSize'
    TOTAL_PAGES = 'TotalPages'
    DATA = 'Data'
    PRICE = 'price'
    VOLUME = 'volume'
    ORDER_TYPE = 'orderType'
    ORDER_GUID = 'OrderGuid'

    def __init__(self):
        super().__init__()
        
        self.__apiKey = str()
        self.__apiSecret = str()
        self.__base = independentreserve()
        self.__base.load_markets()
        deets = self.__base.describe()
        self.__name = deets['name'].lower()
        self.__rateLimit = deets['rateLimit'] / 1000
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
    def Sell(self, primarySecurity = str, secondarySecurity = str, giveAmount = Decimal, receiveAmount = Decimal):
        response = self._BubbleWrapRequest(self.__base.privatePostPlaceLimitOrder, {
            IndependentReserveWrapper.PRIMARY_CURRENCY  : secondarySecurity,
            IndependentReserveWrapper.SECONDARY_CURRENCY : primarySecurity,
            IndependentReserveWrapper.ORDER_TYPE : 'LimitOffer',
            IndependentReserveWraper.PRICE : receiveAmount,
            'volume': giveAmount,
        })

    @overrides
    def ExchangesFeePercentage(self):
        self.__log.info("returning a profit percentage of " + str(self.__profitPercentage))
        return self.__profitPercentage

    @overrides
    def GetOpenOrders(self, primarySecurity = str, secondarySecurity = str, managersName = str):
        pageIndex = 1
        pageSize = 50
        combinedData = []

        while True:
            self.__log.info('Fetching another page of open orders..')
            response = self._BubbleWrapRequest(self.__base.privatePostGetOpenOrders, {
                IndependentReserveWrapper.PRIMARY_CURRENCY  : secondarySecurity,
                IndependentReserveWrapper.SECONDARY_CURRENCY : primarySecurity,
                IndependentReserveWrapper.PAGE_INDEX : str(pageIndex),
                IndependentReserveWrapper.PAGE_SIZE : str(pageSize)
            })
            combinedData += map(self._MapJsonToOrder, response[IndependentReserveWrapper.DATA], managersName)
            self.__log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < response[IndependentReserveWrapper.TOTAL_PAGES]:
                pageIndex += 1

            else:
                return combinedData

    @overrides
    def CancelOrder(self, order = Order):
        """Can return None!"""
        cancelsResponse = self._BubbleWrapRequest(self.__base.cancel_order, order.GetCloudOrderId())
        pageIndex = 1
        pageSize = 50
        combinedData = []

        while True:
            self.__log.info('Fetching another page of partially filled transactions...')
            filledOrdersResponse = self._BubbleWrapRequest(self.__base.privatePostGetClosedFilledOrders, {
                IndependentReserveWrapper.PRIMARY_CURRENCY  : secondarySecurity,
                IndependentReserveWrapper.SECONDARY_CURRENCY : primarySecurity,
                IndependentReserveWrapper.PAGE_INDEX : str(pageIndex),
                IndependentReserveWrapper.PAGE_SIZE : str(pageSize)   
            })

            #combined all partial transactions into one transaction
            for model in filledOrdersResponse[IndependentReserveWrapper.DATA]:
                if model[IndependentReserveWrapper.ORDER_GUID] == order.GetCloudOrderId():
                    combinedData.append(model)

            self.__log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < filledOrdersResponse[IndependentReserveWrapper.TOTAL_PAGES]:
                pageIndex += 1

            elif len(combinedData) > 0:
                return reduce(self._ReduceToTransaction, combinedData)

            else:
                return None

    @overrides
    def ExchangesRateLimit(self):
        return self.__rateLimit

    @overrides
    def _MapJsonToOrder(self, jsonObject = dict, managersName = str):
        marketAction = None
        currentReceivedAount = None
        currentGivenAmount = None

        if jsonObject['OrderType'] == 'LimitOffer':
            marketAction = MarketAction.BUY
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VALUE]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VOLUME]

        else:
            marketAction = MarketAction.SELL
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VOLUME]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VALUE]

        return Order(jsonObject['OrderGuid'], #fixed bug where order guid's label is pascal case
                     managersName,                     
                     jsonObject['SecondaryCurrencyCode'],
                     jsonObject['PrimaryCurrencyCode'],
                     marketAction,
                     currentReceivedAmount,
                     currentGivenAmount,
                     jsonObject['CreatedTimestampUtc'])

    @overrides
    def _ReduceToTransaction(self, wipTransaction = Transaction, jsonObject = dict):
        validatedTransaction = None
           
        if wipTransaction is None:
            validatedTransaction = Transaction()

        else:
            validatedTransaction = wipTransaction

        validatedTransaction.Fill(
            combinedData[0][IndependentReserveWrapper.ORDER_GUID],
            order.GetManagersPair(),
            order.GetOrderState(),
            order.GetPrimarySecurity(),
            order.GetSecondarySecurity(),
            order.GetReceivedAmount(),
            order.GetGivenAmount(),
            order.GetTimeOf()
        )
        return validatedTransaction