from MoonMachine.Trading.RestGateways.NexmoContext import NexmoContext
from MoonMachine.Trading.RestGateways.BitbucketContext import BitbucketContext
from MoonMachine.ModelsModule import Order, LabeledBar, LabeledBarSeries, Transaction
from logging import getLogger

class RecordKeeper(object):
    """description of class"""
    def __init__(self): #fixed bug where the naming convention for constructor was missing an underscore on each side
        self.__notifier = NexmoContext()
        self.BitbucketGateway = BitbucketContext()
        self.log = getLogger(str(self.__class__))

    def Authenticate(self, authCredentials = list):
        authErrors = self.__notifier.AuthenticateNotiferService (authCredentials)
        authErrors += self.BitbucketGateway.TryAuthenticate(authCredentials)
        return authErrors

    def GetTransactions(self):
        return list()

    def GetLastTransaction(self):
        #Transaction.objects.get()
        pass

    def SubmitTransaction(self, transaction = Transaction):
        transaction.save()

    def GetMarketSummaries(self):
        return list()

    def GetOneSummary(self):
        pass

    def SubmitBar(self, bar = LabeledBar):
        pass

    def SubmitSummary(self, summary = LabeledBarSeries):
        pass

    def GetSecondarySecurityExposure(self, marketName):
        result = Transaction.objects.all(market = marketName).latest('date').first()
        self.log.info('Query found transaction from the ' + result.market + '...')
        self.log.info('...a date of ' + str(result.date) + '...')
        self.log.info('...and an exposure of ' + str(currentExposure))
        return result