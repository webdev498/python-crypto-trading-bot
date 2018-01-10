from MoonMachine.Trading.RestGateways.IExchange import IExchange
import requests
from MoonMachine.Models.LabeledBar import LabeledBar
from MoonMachine.Models.LabeledSeries import LabeledSeries
from pyalgotrade.bar import BasicBar, Frequency
from overrides import overrides
import time
import hmac,hashlib
import json
from datetime import datetime

from ccxt.independentreserve import independentreserve

class IndependentReserveContext(IExchange):
    """description of class"""

    def __init__(self):
        super().__init__() 
        self.__publicKey = str
        self.__privateKey = str  
        
    @overrides
    def Name(self): 
        return "independent exchange"
      
    @overrides
    def AuthenticateExchange (self, authDetails = dict, primarySecurity = str, secondarySecurity = str):    
        environmentLabel = ". " + self.Name() + ": ";
        authErrors = str

        try:     
            matchingDetails = authDetails[self.Name()]
            self.__publicKey = matchingDetails[0]
            self.__privateKey = matchingDetails[1]

        except Exception:
            return environmentLabel + "inputfile incorrectly formatted"

        # parameter order must match the documentation
        wipParameters = { 
            'apiKey': self.__publicKey, 
            'nonce': str(inputNonce),  
        }
        
        getAccountsUrl = r"https://api.independentreserve.com/Private/GetAccounts"
        nonce = self.__CreateNonce()
        paramsWithUrl = self.__CreateAuthenticationParamsArray(wipParameters, getAccountsUrl)
        signature = self.__CreateAuthenticationSignature(getAccountsUrl, paramsWithUrl)
        inputData = self.__CreateAuthenticationData(signature, wipParameters)
        inputHeaders = self.__CreateJsonHeader()

        authTest = requests.post (getAccountsUrl, data = json.dumps(inputData, sort_keys = False), headers = inputHeaders)

        if authTest.status_code != requests.codes.ok:
            authErrors = environmentLabel + authTest.json()

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
       
    def __CreateAuthenticationSignature(self, url = str, finalParameters = []):
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

        for datedLabel in commitLabels:
            if datedLabel.Label.lower().find ("label:") == -1:
                datedLabels.remove(datedLabel)

        labeledSeries = LabeledSeries([labeledSummary], datedLabels)
        return labeledSeries
    
    @overrides
    def Buy(self, securityToReceive = str, securityToGive = str):
        pass

    @overrides
    def Sell(self, securityToGive = str, securityToReceive = str):
        pass