from MoonMachine.Trading.RestGateways.NexmoContext import NexmoContext
from MoonMachine.Trading.RestGateways.BitbucketContext import BitbucketContext
from MoonMachine.Models.Order import Order
from MoonMachine.Models.LabeledBar import LabeledBar
from MoonMachine.Models.LabeledBarSeries import LabeledBarSeries
from MoonMachine.Models.Transaction import Transaction

class RecordKeeper(object):
    """description of class"""
    def __init__(self): #fixed bug where the naming convention for constructor was missing an underscore on each side
        self.__notifier = NexmoContext()
        self.BitbucketGateway = BitbucketContext()

    def Authenticate(self, authCredentials = list):
        authErrors = self.__notifier.AuthenticateNotiferService (authCredentials)
        authErrors += self.BitbucketGateway.TryAuthenticate(authCredentials)
        return authErrors

    def GetTransactions(self):
        return list()

    def GetOnetransaction(self):
        return Order()

    def SubmitTransaction(self, transaction = Transaction):
        pass

    def GetMarketSummaries(self):
        return list()

    def GetOneSummary(self):
        pass

    def SubmitBar(self, bar = LabeledBar):
        pass

    def SubmitSummary(self, summary = LabeledBarSeries):
        pass