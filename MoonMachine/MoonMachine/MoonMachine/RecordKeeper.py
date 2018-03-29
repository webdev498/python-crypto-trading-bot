from MoonMachine.ModelsModule import Order, LabeledBar, LabeledBarSeries, Transaction, MarketInfo

from logging import getLogger
from decimal import Decimal

from django.contrib.auth.models import User
from django.http.request import HttpRequest


class RecordKeeper(object):
    """description of class"""
    def __init__(self): #fixed bug where the naming convention for constructor was missing an underscore on each side
        self.__log = getLogger(str(self.__class__))

    def Authenticate(self, authCredentials = list):
        return ""

    def GetTransactions(self):
        raise NotImplementedError()

    def GetLastTransaction(self):
        """Can return None!"""
        query = Transaction.objects.order_by('date')

        if query:
            return query.last() #negative sign returns results in descending order

        else:
            return None

    def SubmitTransaction(self, transaction = Transaction):
        currentExposure = Decimal()
        currentUser = GetCurrentUser()

        if transaction.marketAction == MarketAction.BUY:
            currentExposure += transaction.receivedAmount

        elif transaction.marketAction == MarketAction.SELL:
            currentExposure -= transaction.receivedAmount
        
        possibleExisting = MarketInfo.objects.filter(marketPair = transaction.marketPair, user_id = transaction.user)

        if possibleExisting:
            match = possibleExisting.first()
            match.currentExposure = currentExposure
            match.save()

        else:
            MarketInfo().Fill(transaction.user, transaction.marketPair, currentExposure).save()

        transaction.save()

    def GetMarketSummaries(self):
        raise NotImplementedError()

    def GetOneMarketSummary(self):
        raise NotImplementedError()

    def SubmitLabeledBar(self, bar = LabeledBar):
        raise NotImplementedError()

    def SubmitMarketSummary(self, summary = LabeledBarSeries):
        raise NotImplementedError()

    def GetMarketInfo(self, marketName = str, currentUserId = int):
        """Can return None!"""

        possibleMatch = MarketInfo.objects.filter(marketPair = marketName, user_id = currentUserId)

        if possibleMatch:
            self.__log.info('found matching market summary.')
            result = possibleMatch.first()
            return result

        else:
            self.__log.warning('no matching market summary found!')
            return None