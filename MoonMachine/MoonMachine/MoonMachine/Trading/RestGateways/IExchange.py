import requests
from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar, Bar
from abc import ABC, abstractmethod, abstractproperty
from MoonMachine.Trading.RestGateways.BitbucketContext import BitbucketContext

class IExchange(ABC):
    """base class"""

    def __init__(self):
        super().__init__()
        pass      

    @abstractmethod
    def GetMarketUpdate(self, lastKnownBar = Bar, labels = list, primarySecurity = str, secondarySecurity = str):
        pass

    @abstractproperty
    def Name(self):
        pass

    @abstractmethod
    def AuthenticateExchange (self, authDetails = dict, primarySecurity = str, secondarySecurity = str):
        pass

    @abstractmethod
    def Buy(self, securityToReceive = str, securityToGive = str):
        pass

    @abstractmethod
    def Sell(self, securityToGive = str, securityToReceive = str):
        pass