from MoonMachine.Trading.RestGateways.IExchange import IExchange
from MoonMachine.Trading.RecordKeeper import RecordKeeper
from pyalgotrade.bar import Bar
from MoonMachine.Models.LabeledBarSeries import LabeledBarSeries
from MoonMachine.Models.DatedLabel import DatedLabel
from MoonMachine.SelectionOptions.ApplicationStatus import ApplicationStatus
from logging import logger

class MarketManager(object):
    """description of class"""
    def __init__(self, primarySecurity = str(), secondarySecurity = str(), exchangeInstance = IExchange): #fixed bug where params were in the wrong order
        self.__primarySecurity = primarySecurity
        self.__secondarySecurity = secondarySecurity
        self.__exchange = exchangeInstance
        self.__recordKeeper = RecordKeeper()
        self.IsAuthenticated = False
        self.__authAppStatus = ApplicationStatus.NOT_SUBMITTED

    def Work(self):
        if self.IsAuthenticated:
            marketHistory = self.__recordKeeper.GetMarketSummaries()
            historyLength = len(marketHistory)            
            lastKnownBar = Bar() if historyLength == 0 else marketHistory[historyLength - 1]
            #self.__exchange.GetMarketUpdate(lastKnownBar, self.__primarySecurity, self.__secondarySecurity)
            #test = LabeledBarSeries([Bar(), Bar()], [DatedLabel()])

    def AttemptAuthentication(self,
                              serviceCredentials = dict()):
        self.__authAppStatus = ApplicationStatus.PROCESSING
        authErrors = self.__exchange.AuthenticateExchange(serviceCredentials, self.__primarySecurity, self.__secondarySecurity)
        authErrors += self.__recordKeeper.Authenticate(serviceCredentials)
        self.__authAppStatus = ApplicationStatus.PROCESSED

        if authErrors == "":
            self.IsAuthenticated = True

        return authErrors 

    def GetAuthAppStatus(self):
        return self.__authAppStatus