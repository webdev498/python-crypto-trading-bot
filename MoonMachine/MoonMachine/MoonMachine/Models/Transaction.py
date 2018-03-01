from django.db import models
from MoonMachine.SelectionOptions.ModelLimits import *
from MoonMachine.SelectionOptions.MarketAction import MarketAction
from datetime import datetime
from decimal import Decimal
import csv
from io import StringIO

class Transaction(models.Model):
    marketAction = models.CharField(max_length=4)

    primarySecurity = models.CharField(max_length=4)
    secondarySecurity = models.CharField(max_length=4)
    receivedAmount = models.DecimalField()
    givenAmount = models.DecimalField()

    date = models.DateField()
    currentExposure = models.FloatField()
    misc = models.CharField()

    def __init__(self, state = MarketAction, inputPrimarySecurity = str, inputSecondarySecurity = str, inputReceivedAmount = Decimal, inputGivenAmount = Decimal, inputTransactionTime = datetime, inputPeviousExposure = Decimal **kwargs):
        if state == MarketAction.HOLD:
            getLogger().error("A transaction cannot have the state: " + str(MarketAction.HOLD))
            raise Exception()

        marketAction = state

        self.primarySecurity = inputPrimarySecurity
        self.secondarySecurity = inputSecondarySecurity
        self.receivedAmount = inputReceivedAmount
        self.givenAmount = inputGivenAmount

        self.date = inputTransactionTime
        self.currentExposure = inputPeviousExposure

        if self.marketAction == MarketAction.BUY:
            self.currentExposure += self.receivedAmount

        else:
            self.currentExposure -= self.receivedAmount

        fileLikeObj = StringIO()
        serialiser = csv.writer(fileLikeObj)

        for row in kwargs:
            self.misc = serialiser.writerow()
