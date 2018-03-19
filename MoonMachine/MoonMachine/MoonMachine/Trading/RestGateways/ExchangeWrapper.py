import requests
from pyalgotrade.dataseries.bards import BarDataSeries
from pyalgotrade.bar import BasicBar, Bar
from abc import ABC, abstractmethod, abstractproperty

from MoonMachine.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries

from pyalgotrade.bar import BasicBar, Frequency
from overrides import overrides
import time
import hmac,hashlib
import json
from datetime import datetime
import logging
from decimal import Decimal
from logging import getLogger, Logger

from ccxt import independentreserve, Exchange

class ExchangeWrapper(object):
    """base class"""

    def __init__(self, injectedExchange = Exchange, profitPercentage = Decimal):        
        self.__log = getLogger(str(self.__class__))
        self.__profitPercentage = profitPercentage
        self.__exchange = injectedExchange

    def AttemptAuthentication(self, authDetails = dict):
        try:            
            self.__exchange.apiKey = authDetails['independent reserve']['apiKey']
            self.__exchange.secret = authDetails['independent reserve']['secret']

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.__exchange.name + ". " + str(e)
            self.__log.error(error)
            return error

        try:
            self.__exchange.fetch_balance()

            return ''

        except Exception as e:
            error = 'authentication failed using given apiKey and secret for exchange: ' + self.__exchange.name + ". " + str(e)
            self.__log(error)
            return error

    def GetMarketUpdate(self, lastKnownBar = Bar, labels = list, primarySecurity = str, secondarySecurity = str):
        try:
            response = self.__exchange.fetch_ticker(secondarySecurity + "/" + primarySecurity)     
            return response

        except Exception as e:
            self.__log.error("exception occured while fetching market update: " + str(e))
            raise
        pass
    
    def Buy(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    
    def Sell(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    
    def ExchangesMinimumProfitPercentage(self):
        raise NotImplementedError()

    
    def GetOpenOrders(self):
        raise NotImplementedError()

    
    def CancelOrder(self, order = Order):
        raise NotImplementedError()