from django.db import models
from MoonMachine.SelectionOptions.ModelLimits import *
from MoonMachine.SelectionOptions.MarketAction import MarketAction
from datetime import datetime

class Transaction(object):
    def __init__(self, state = MarketAction, receivedAmount = int, givenAmount = int, TransactionTime = datetime, **kwargs):
        if state == MarketAction.HOLD:
            getLogger().error("A transaction cannot have the state: " + str(MarketAction.HOLD))
            raise Exception()

        self.__tradeState = state
        self.__receivedAmount = receivedAmount
        self.__GivenAmount = givenAmount
        self.__transactionTime = TransactionTime
        self.__miscellaneous = kwargs

    def GetOrderState(self):
        return self.__tradeState

    def GetReceivedAmount(self):
        return self.__receivedAmount

    def GetGivenAmount(self):
        return self.__GivenAmount

    def GetTimeOf(self):
        return self.__transactionTime

    def GetMiscellaneousProperties(self):
        return self.__miscellaneous
