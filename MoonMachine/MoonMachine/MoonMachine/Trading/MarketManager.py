from MoonMachine.RecordKeeper import RecordKeeper
from MoonMachine.Trading.RestGateways.ExchangeWrapper import ExchangeWrapper
from MoonMachine.ModelsModule import LabeledBarSeries, DatedLabel, Order
from MoonMachine.Trading.Strategy.ExecutiveAnalyzer import ExecutiveAnalyzer

from pyalgotrade.bar import Bar
from ccxt import Exchange

import logging
from decimal import Decimal

class MarketManager(object):
    """description of class"""
    def __init__(self, primarySecurity = str, secondarySecurity = str, exchangeInstance = Exchange): #fixed bug where params were in the wrong order
        self.__log = logging.getLogger(str(self.__class__))
        self.__log.info('creating new market manager.')
        self.__primarySecurity = primarySecurity
        self.__secondarySecurity = secondarySecurity
        self.__exchange = ExchangeWrapper (exchangeInstance, Decimal(0.02))
        self.__recordKeeper = RecordKeeper()
        self.__executiveAnalyzer = ExecutiveAnalyzer()
        self.__isAuthenticated = False        
        self.__managerName = exchangeInstance.name + " " + secondarySecurity + '/' + primarySecurity
        self.__log.info('marketManager created.')

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
            self.__log.info("Beginning disposal of the " + self.__primarySecurity + " / " + self.__secondarySecurity + " market.")
            cloudOpenOrders = self.__exchange.GetOpenOrders()

            #close open orders
            for order in cloudOpenOrders:
                previousTransaction = self.__exchange.GetMarketUpdate()

                if order.GetOrderState() == Order.BUY:
                    self.__log.info("Cancelling open buy order.")
                    possibleCompletion = self.__exchange.CancelOrder(order, previousTransaction)

                    if possibleCompletion != None:
                        self.__recordKeeper.SubmitTransaction(possibleCompletion)
                       
            #market exposure
            minimumProfit = self.__exchange.ExchangesMinimumProfitPercentage()
            marketExposure = self.__recordKeeper.GetSecondarySecurityExposure((self.__exchange.__class__))
            salePrice = self.__executiveAnalyzer.GetMinimumProfitPrice(marketExposure, minimumProfit)           
            disposalSale = self.__exchange.Sell(self.__secondarySecurity, self.__primarySecurity, marketExposure, salePrice)                                       
            cloudOpenOrders.append(disposalSale)

        else:
            self.__log.info("Market manager was not authenticated. Did not dispose.")