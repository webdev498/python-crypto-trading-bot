from MoonMachine.Trading.RestGateways.IExchange import IExchange
from MoonMachine.Trading.RecordKeeper import RecordKeeper
from pyalgotrade.bar import Bar

class MarketManager(object):
    """description of class"""
    def __init__(self, primarySecurity = str, secondarySecurity = str, exchangeInstance = IExchange): #fixed bug where params were in the wrong order
        self.__primarySecurity = primarySecurity
        self.__secondarySecurity = secondarySecurity
        self.__exchange = exchangeInstance
        self.__recordKeeper = RecordKeeper()
        self.IsAuthenticated = False

    def Work(self):
        if self.__IsAuthenticated:
            marketHistory = self.__recordKeeper.GetMarketHistory()
            lastKnownBar = marketHistory[marketHistory.count() - 1]
            self.__exchange.GetMarketUpdate(lastKnownBar, self.__primarySecurity, self.__secondarySecurity)

    def AttemptAuthentication(self,
                              serviceCredentials = dict):
        authErrors = self.__exchange.AuthenticateExchange(serviceCredentials, self.__primarySecurity, self.__secondarySecurity)
        authErrors += self.__recordKeeper.Authenticate(serviceCredentials)

        if authErrors == "":
            self.IsAuthenticated = True

        return authErrors 