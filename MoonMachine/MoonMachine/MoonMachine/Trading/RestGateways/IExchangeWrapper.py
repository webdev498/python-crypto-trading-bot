from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar, Bar
from abc import ABC, abstractmethod, abstractproperty
from MoonMachine.ModelsModule import Order, Transaction
from decimal import Decimal
from functools import partial
from time import sleep
from logging import getLogger

class IExchangeWrapper(ABC):
    """description of class"""
    def __init__(self):
        self.__log = getLogger(str(self.__class__))
        super().__init__()    

    @abstractmethod
    def Name(self):
        raise NotImplementedError()

    @abstractmethod
    def AttemptAuthentication(self, authDetails = dict):
        raise NotImplementedError()

    @abstractmethod
    def GetMarketUpdate(self, lastKnownBar = Bar, labels = list, pairsSymbol = str):
        raise NotImplementedError()

    @abstractmethod
    def Buy(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def Sell(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def ExchangesFeePercentage(self):
        raise NotImplementedError()

    @abstractmethod
    def GetOpenOrders(self, primarySecurity = str, secondarySecuity = str, managersName = str):        
        raise NotImplementedError()

    @abstractmethod
    def CancelOrder(self, order = Order):
        raise NotImplementedError() 

    @abstractmethod
    def ExchangesRateLimit(self):
        raise NotImplementedError()

    def _BubbleWrapRequest(self, function, *args): #one dash to allow access to derived classes
        try:
            sleep(self.ExchangesRateLimit())
            partiallyFilledFunction = partial(function, *args)
            return partiallyFilledFunction()
            
        except Exception as e:
            self.__log.error(self.Name() + "something went wrong while requesting an exchange: " + str(e))

    @abstractmethod
    def _MapJsonToOrder(self, jsonObject = dict):
        raise NotImplementedError()
    
    @abstractmethod
    def _ReduceToTransaction(self, wipTransaction = Transaction, jsonObject = dict):
        raise NotImplementedError()