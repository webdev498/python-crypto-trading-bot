import requests
from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar, Bar
from abc import ABC, abstractmethod, abstractproperty
from MoonMachine.Trading.RestGateways.BitbucketContext import BitbucketContext
from MoonMachine.ModelsModule import Order
from decimal import Decimal

class IExchange(ABC):
    """base class"""

    def __init__(self):
        super().__init__()    

    @abstractmethod
    def GetMarketUpdate(self, lastKnownBar = Bar, labels = list, primarySecurity = str, secondarySecurity = str):
        raise NotImplementedError()

    @abstractmethod
    def AuthenticateExchange (self, authDetails = dict, primarySecurity = str, secondarySecurity = str):
        raise NotImplementedError()

    @abstractmethod
    def Buy(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def Sell(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def ExchangesMinimumProfitPercentage(self):
        raise NotImplementedError()

    @abstractmethod
    def GetOpenOrders(self):
        raise NotImplementedError()

    @abstractmethod
    def CancelOrder(self, order = Order):
        raise NotImplementedError()