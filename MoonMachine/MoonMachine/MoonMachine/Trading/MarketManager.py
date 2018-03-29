from MoonMachine.RecordKeeper import RecordKeeper
from MoonMachine.Trading.RestGateways.IExchangeWrapper import IExchangeWrapper
from MoonMachine.ModelsModule import LabeledBarSeries, DatedLabel, Order
from MoonMachine.Trading.Strategy.ExecutiveAnalyzer import ExecutiveAnalyzer

from pyalgotrade.bar import Bar

import logging
from decimal import Decimal
from django.http.request import HttpRequest

class MarketManager(object):
    """description of class"""
    def __init__(self, primarySecurity = str, secondarySecurity = str, exchangeInstance = IExchangeWrapper): #fixed bug where params were in the wrong order
        self.__log = logging.getLogger(str(self.__class__))
        self.__primarySecurity = primarySecurity #placed here since it controls which item to buy / sell. makes exchangewrapper a little more universal
        self.__secondarySecurity = secondarySecurity
        self.__exchange = exchangeInstance
        self.__recordKeeper = RecordKeeper()
        self.__executiveAnalyzer = ExecutiveAnalyzer()
        self.__isAuthenticated = False   
        pairsSymbol = str.capitalize(primarySecurity + "/" + secondarySecurity)
        self.__managerName = exchangeInstance.Name() + " " + pairsSymbol

        #volatile injections
        self.__multiThreadedRequest = None

        self.__log.info('marketManager created.')

    def SetRequestObject(self, injectedObject = HttpRequest):
        self.__multiThreadedRequest = injectedObject

    def GetManagerName(self):
        return self.__managerName

    def Work(self):
        if self.__isAuthenticated:
            #marketHistory = self.__recordKeeper.GetMarketSummaries()
            #historyLength = len(marketHistory)            
            #lastKnownBar = Bar() if historyLength == 0 else marketHistory[historyLength - 1]
            #self.__exchange.GetMarketUpdate(lastKnownBar, self.__primarySecurity, self.__secondarySecurity)
            #test = LabeledBarSeries([Bar(), Bar()], [DatedLabel()])
            pass

    def AttemptAuthentication(self, serviceCredentials = dict):
        authErrors = self.__exchange.AttemptAuthentication(serviceCredentials)
        authErrors = authErrors + self.__recordKeeper.Authenticate(serviceCredentials)

        if authErrors == "":
            self.__isAuthenticated = True

        else:
            self.__isAuthenticated = False

        return authErrors 

    def IsAuthenticated(self):
        return self.__isAuthenticated

    def Dispose(self):
        if self.__isAuthenticated:
            self.__log.info("Beginning disposal of the " + self.GetManagerName() + " market.")
            cloudOpenOrders = self.__exchange.GetOpenOrders(self.__primarySecurity, self.__secondarySecurity, self.GetManagerName())

            #close open orders
            for order in cloudOpenOrders:                
                if order.GetOrderState() == Order.BUY:
                    self.__log.info("Cancelling open buy order.")
                    possibleCompletion = self.__exchange.CancelOrder(order)

                    if possibleCompletion != None:
                        possibleCompletion.user_id = self.__multiThreadedRequest.user.id
                        self.__recordKeeper.SubmitTransaction(possibleCompletion)
                       
            #market exposure
            fee = self.__exchange.ExchangesFeePercentage()
            possibleMarketInfo = self.__recordKeeper.GetMarketInfo(self.__exchange.Name(), self.__multiThreadedRequest.user.id)
            marketExposure = Decimal()

            if possibleMarketInfo is not None:
                marketExposure = possibleMarketInfo.currentExposure

            salePrice = self.__executiveAnalyzer.GetMinimumProfitPrice(marketExposure, fee)           
            disposalSale = self.__exchange.Sell(self.__secondarySecurity, self.__primarySecurity, marketExposure, salePrice)                                       

        else:
            self.__log.info("Market manager was not authenticated. Did not dispose.")

        self.SetRequestObject(None)