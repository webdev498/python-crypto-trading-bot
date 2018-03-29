from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.http.request import HttpRequest

from MoonMachine.SelectionOptions.ModelLimits import *
from MoonMachine.SelectionOptions.MarketAction import MarketAction

from datetime import datetime
from decimal import Decimal
import csv
from io import StringIO
from logging import Logger, getLogger

from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar

from collections.abc import MutableSequence
from overrides import overrides

################################################
##DATABASE TABLES
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False)
    transactionId = models.CharField(max_length = FAIR_STRING_SIZE)

    marketPair = models.CharField(max_length = FAIR_STRING_SIZE)
    marketAction = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)

    primarySecurity = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    secondarySecurity = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    receivedAmount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)
    givenAmount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)
    date = models.DateField()    

    def Fill(self, inputUserId = int, inputTransactionId = str, inputMarketPair = str, state = MarketAction, inputPrimarySecurity = str, inputSecondarySecurity = str, inputReceivedAmount = Decimal, inputGivenAmount = Decimal, inputTransactionTime = datetime, **kwargs):
        log = getLogger(str(self.__class__)) # temporary variable since I have no idea what will happen if you store a property on a database record
        log.info('filling transaction object...')
        self.user_id = inputUserId
        self.transactionId = inputTransactionId

        if state == MarketAction.HOLD:
            log.error("A transaction cannot have the state: " + MarketAction.HOLD)
            raise Exception()

        self.marketPair = inputMarketPair
        self.marketAction = state

        self.primarySecurity = inputPrimarySecurity
        self.secondarySecurity = inputSecondarySecurity
        self.receivedAmount = inputReceivedAmount
        self.givenAmount = inputGivenAmount

        self.date = inputTransactionTime
        self.save()
        log.info('Transaction ' + str(self.date) + ' filled')

class MarketInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False) #settings.AUTH_USER_MODEL is the correct convention for referring to the currently logged in user

    marketPair = models.CharField(max_length = FAIR_STRING_SIZE)
    currentExposure = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)
    miscellaneous = models.CharField(max_length = SERIALIZED_DATA_LIMIT)

    def Fill(self, userId = int, inputMarketPair = str, inputExposure = Decimal, **kwargs):
        log = getLogger(str(self.__class__))
        log.info('filling market info object...')
        self.user_id = userId

        if inputMarketPair:
            self.marketPair = inputMarketPair

        if inputExposure:
            self.currentExposure = inputExposure

        if kwargs is not None: #kwargs default state
            with StringIO() as fileLikeObj:
                log.info('serializing ' + str(len(kwargs)) + ' key word arguments to csv.')
                serialiser = csv.writer(fileLikeObj, delimiter='#')
                keyWordItems = kwargs.items()

                for key, value in keyWordItems:
                    serialiser.writerow([key, value])
                
                writersValues = fileLikeObj.getvalue()
                valuesLength = len(writersValues)
                finalLength = valuesLength + 1
                stringsToJoin = [] * finalLength

                if self.miscellaneous is not None:
                    stringsToJoin[0] = self.miscellaneous

                for index in range(valuesLength): #range starts from 0 and ends one before the stop argument
                    correctedIndex = index + 1 if index != valuesLength - 1 else index
                    stringsToJoin[correctedIndex] = writersValues[index] # im building self.misc this way because this string has the potential to greatly impact performance.

                self.miscellaneous = str().join(stringsToJoin)
                
        self.save()
        log.info('filled the market info object.')


##################################################
##BACKEND ONLY MODELS
class Order(object):    
    """orders must have enough information to convert to a transaction."""
    def __init__(self, cloudOrderId = int, managersPairSymbol = str, primarySecurity = str, secondarySecurity = str, state = MarketAction, inputReceivedAmount = Decimal, inputGivenAmount = Decimal, inputOrderTime = datetime, **kwargs):
        if state == MarketAction.HOLD:
            getLogger().error("An order cannot have the state: " + str(MarketAction.HOLD))
            raise Exception()

        self.__cloudOrderId = cloudOrderId
        self.__pairsSymbol = managersPairSymbol
        self.__primary = primarySecurity
        self.__secondary = secondarySecurity
        self.__orderState = state
        self.__receivedAmount = receivedAmount
        self.__GivenAmount = givenAmount
        self.__orderTime = orderTime
        self.__miscellaneous = kwargs

    def GetCloudOrderId(self):
        return self.__cloudOrderId

    def GetManagersPair(self):
        return self.__pairsSymbol

    def GetPrimarySecurity(self):
        return self.__primary

    def GetSecondarySecurity(self):
        return self.__secondary

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

class LabeledBar(object):
    def __init__(self, bar = BasicBar, labels = list):   
        self.Labels = labels  
        self.Bar = bar

class DatedLabel(object):
    """Date will be rounded down to the nearest hour."""
    def __init__(self, date = datetime, label = str):
        self.Date = date
        self.Label = str

class LabeledBarSeries(MutableSequence):
    def __init__(self, listOfNormalBars = list, listOfDatedLabels = list):
        """creates a series of LabeledBars by tagging bars with their closest labels. datetimes are automatically rounded down to the nearest day."""
        super().__init__()
        self.UnderlyingBars = BarDataSeries()
        self.__combined = list()
        self.__log = Logger(str(self.__class__))
        self.__log.info("constructing.")

        for currentBar in listOfNormalBars:
            self.UnderlyingBars.append(currentBar)
            labeledBarWip = LabeledBar(currentBar, [])
            barsDate = labeledBarWip.Bar.getDateTime()

            for datedLabel in listOfDatedLabels:
                #datetimes are immutable
                datedLabel.Date = datetime.replace(datedLabel.Date, hour = 0, minute = 0, second = 0, microsecond = 0) #im using a class method version in order to get at design time intellisense of a boxed datetime

                if datedLabel.Date <= barsDate: #assuming bar dates are ordered                    
                    self.__removePreviousOccurrencesOfLabel(datedLabel.Label) 
                    labeledBarWip.Labels.append(datedLabel.Label)

            self.__combined.append(labeledBarWip)         
            
        self.__log.info(str(self.__class__) + "constructed. ")

    def __removePreviousOccurrencesOfLabel(self, label = str):
        counter = 0

        for removalBar in self.__combined:
            for comparisonLabel in reverse(removalBar.Labels): #removing in reverse order ensures that the working index does not change
                if comparisonLabel == label:
                    counter += 1
                    removalBar.Labels.remove(comparisonLabel)

        self.__log.info("Duplicate labels of title '" + label + "' removed: " + str(counter))

    @overrides
    def append(self, value = LabeledBar):
        self.__combined.append(value)

    @overrides
    def clear(self):
        self.__combined.clear()

    @overrides
    def count(self, value):
        self.__log.error("count override not supported")
        raise NotImplementedError()

    @overrides
    def extend(self, values = list):
        self.__combined.extend(list)

    @overrides
    def index(self, value, start = 0, stop = None):
        return self.__combined.index(value, start, stop)

    @overrides
    def insert(self, index, value):
        self.__combined.insert(index, value)

    @overrides
    def pop(self, index):
        return self.__combined.pop(index)

    @overrides
    def remove(self, value):
        self.__combined.remove(value)

    @overrides
    def reverse(self):
        self.__combined.reverse()

    @overrides
    def __delitem__(self, index):
        self._combined.remove(index)

    @overrides 
    def __setitem__(self, index, value):
        self.__combined[index] = value

    def __len__(self):
        return len(self.__combined)

    def __getitem__(self, index):
        return self.__combined[index]

