from MoonMachine.Trading.RestGateways.IExchange import IExchange
from MoonMachine.Trading.RecordKeeper import RecordKeeper
from pyalgotrade.bar import Bar
from MoonMachine.Models.LabeledBarSeries import LabeledBarSeries
from MoonMachine.Models.DatedLabel import DatedLabel
import logging
from MoonMachine.Models.Order import Order
from MoonMachine.Trading.Strategy.ExecutiveAnalyzer import ExecutiveAnalyzer
import logging

class MarketManager(object):
    """description of class"""
    def __init__(self, primarySecurity = str, secondarySecurity = str, exchangeInstance = IExchange): #fixed bug where params were in the wrong order
        self.__primarySecurity = primarySecurity
        self.__secondarySecurity = secondarySecurity
        self.__exchange = exchangeInstance
        self.__recordKeeper = RecordKeeper()
        self.__executiveAnalyzer = ExecutiveAnalyzer()
        self.__isAuthenticated = False
        self.__log = logging.getLogger(str(self.__class__))

    def Work(self):
        if self.__isAuthenticated:
            #wip
            marketHistory = self.__recordKeeper.GetMarketSummaries()
            historyLength = len(marketHistory)            
            lastKnownBar = Bar() if historyLength == 0 else marketHistory[historyLength - 1]
            #self.__exchange.GetMarketUpdate(lastKnownBar, self.__primarySecurity, self.__secondarySecurity)
            #test = LabeledBarSeries([Bar(), Bar()], [DatedLabel()])

    def AttemptAuthentication(self, serviceCredentials = dict):
        authErrors = self.__exchange.AuthenticateExchange(serviceCredentials, self.__primarySecurity, self.__secondarySecurity)
        authErrors += self.__recordKeeper.Authenticate(serviceCredentials)

        if authErrors == "":
            self.__isAuthenticated = True

        return authErrors 

    def IsAuthenticated(self):
        return self.__isAuthenticated

    def Dispose(self):
        if self.__isAuthenticated:
            self.__log.info("Beginning disposal of the " + self.__primarySecurity + " / " + self.__secondarySecurity + " market.")
            cloudOpenOrders = self.__exchange.GetOpenOrders()
            localOpenOrders = self.__recordKeeper.GetOpenOrders()

            #close open orders
            for order in cloudOpenOrders:
                if order.GetOrderState() == Order.BUY:
                    self.__log.info("Cancelling open buy order.")
                    possibleCompletion = self.__exchange.CancelOrder(order)

                    if possibleCompletion != None:
                        self.__recordKeeper.SubmitTransaction(possibleCompletion)
                       
            #market exposure
            self.__log.info("Defaulting market exposure.")
            minimumProfit = self.__exchange.ExchangesMinimumProfitPercentage()
            salePrice = self.__executiveAnalyzer.GetMinimumProfitPrice(latestTrade, minimumProfit)           
            disposalSale = self.__exchange.Sell(self.__primarySecurity, self.__secondarySecurity, latestTrade.GetReceivedAmount(), salePrice)                                       
            cloudOpenOrders.append(disposalSale)

        else:
            self.__log("Market manager was not authenticated. Did not dispose.")