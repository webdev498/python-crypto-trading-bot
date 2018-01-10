from MoonMachine.Trading.RestGateways.NexmoContext import NexmoContext
from MoonMachine.Trading.RestGateways.BitbucketContext import BitbucketContext

class RecordKeeper(object):
    """description of class"""
    def __init__(self): #fixed bug where the naming convention for constructor was missing an underscore on each side
        self.__notifier = NexmoContext()
        self.BitbucketGateway = BitbucketContext()

    def Authenticate(self, authCredentials = []):
        authErrors = self.__notifier.AuthenticateNotiferService (authCredentials)
        authErrors += self.BitbucketGateway.TryAuthenticate(authCredentials)
        return authErrors

    def GetTradeDecisions(self):
        pass

    def GetMarketSummaries(self):
        return []

    def GetOneSummary(self, index = int):
        pass

