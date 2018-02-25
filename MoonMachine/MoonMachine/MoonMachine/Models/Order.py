from django.db import models
import MoonMachine.SelectionOptions.ModelLimits
from MoonMachine.SelectionOptions.MarketAction import MarketAction
from datetime import datetime
from logging import *

class Order(object):    
    def __init__(self, state = MarketAction, receivedAmount = int, givenAmount = int, orderTime = datetime, **kwargs):
        if state == MarketAction.HOLD:
            getLogger().error("An order cannot have the state: " + str(MarketAction.HOLD))
            raise Exception()

        self.__orderState = state
        self.__receivedAmount = receivedAmount
        self.__GivenAmount = givenAmount
        self.__orderTime = orderTime
        self.__miscellaneous = kwargs

    def GetOrderState(self):
        return self.__orderState

    def GetReceivedAmount(self):
        return self.__receivedAmount

    def GetGivenAmount(self):
        return self.__GivenAmount

    def GetTimeOf(self):
        return self.__orderTime

    def GetMiscellaneousProperties(self):
        return self.__miscellaneous
