from MoonMachine.Trading.RestGateways.IExchange import IExchange
import requests

from MoonMachine.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries

from pyalgotrade.bar import BasicBar, Frequency
from overrides import overrides
import time
import hmac,hashlib
import json
from datetime import datetime
import logging
from decimal import Decimal

from ccxt.independentreserve import independentreserve
import ccxt

class IndependentReserveContext(IExchange):
    """description of class"""

    def __init__(self):
        super().__init__()
        
        self.__apiKey = str()
        self.__apiSecret = str()
        self.__nonce = str()

        self.__log = logging.getLogger(str(self.__class__))
        self.__profitPercentage = Decimal('0.02')
        self.__base = independentreserve()

    @overrides
    def AuthenticateExchange (self, authDetails = dict, primarySecurity = str, secondarySecurity = str):
        environmentLabel = ". " + str(self.__class__) + ": "
        authErrors = str()   
        return authErrors

    def __CreateNonce(self):
        return int(time.time())

    def __CreateAuthenticationParamsArray(self, parameterPairs = dict, url = str):
        """parametersPairs must be string keys and values"""
        outputList = list()
        outputList.append(url)

        for item in parameterPairs.items():
            newItem = item[0] + "=" + item[1]
            outputList.append(newItem)

        return outputList

    def __CreateAuthenticationSignature(self, url = str, finalParameters = list):
        message = ','.join(finalParameters)

        signature = hmac.new(self.__privateKey.encode('utf-8'),
                            msg = message.encode('utf-8'),
                            digestmod = hashlib.sha256).hexdigest().upper()

        return signature

    def __CreateAuthenticationData(self, signature = str, parameterPairs = dict):
        authData = {"signature": signature}

        for item in parametersList:
            authData[item[0]] = item[1]

        return authData

    def __CreateJsonHeader(self):
        return {'Content-Type': 'application/json'}

    @overrides
    def GetMarketUpdate(self, lastKnownBar = BasicBar, labels = list, primarySecurity = str, secondarySecurity = str):
        """Returns a LabeledBar of todays market summary."""
        requestLocator = r"https://api.independentreserve.com/Public/GetMarketSummary?primarycurrencycode=" + primarySecurity + "&secondarycurrencycode=" + secondarySecurity
        response = requests.get (requestLocator)
        jsonResult = response.json()
        dateBarCreated = jsonResult['CreatedTimestampUtc']
        DayHighestPrice = jsonResult['DayHighestPrice']
        DayLowestPrice = jsonResult['DayLowestPrice']
        DayVolumeXbt = jsonResult['DayVolumeXbt']
        LastPrice = jsonResult['LastPrice']

        dateBarCreated = datetime.utcfromtimestamp(dateBarCreated)

        rawSummary = BasicBar(dateBarCreated,
                                lastKnownBar.getClose(),
                                DayHighestPrice,
                                DayLowestPrice,
                                LastPrice,
                                DayVolumeXbt,
                                LastPrice,
                                0,
                                None)

        labeledSeries = LabeledBarSeries([labeledSummary], labels)
        return labeledSeries

    @overrides
    def Buy(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def Sell(self, securityToGive = str, securityToReceive = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def ExchangesMinimumProfitPercentage(self):
        self.__log.info("returning a profit percentage of " + str(self.__profitPercentage))
        return self.__profitPercentage

    @overrides
    def GetOpenOrders(self):
        return list()

    @overrides
    def CancelOrder(self, order = Order):
        return Transaction()