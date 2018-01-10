import time
import hmac,hashlib
import json

from threading import Thread
from MoonMachine.Trading.RestGateways.IndependentReserveContext import IndependentReserveContext
from MoonMachine.Trading.MarketManager import MarketManager
from MoonMachine.SelectionOptions.LabeledConstants import *

class ParallelTrader(Thread):
    START_STATE = 'Start'
    STOP_STATE = 'Stop'

    def __init__(self):
        Thread.__init__(self)        
        self.ToggleSwitchesState = ParallelTrader.START_STATE
        self.__continueRunning = bool

        self.__portfolio = [
            MarketManager(XBT_STRING, AUD_STRING, IndependentReserveContext()),
        ]

    def run(self):
        self.ToggleSwitchesState = ParallelTrader.STOP_STATE      
        self.__continueRunning = True

        while self.__continueRunning:              
            for market in self.__portfolio:
                market.Work()

        self.ToggleSwitchesState = ParallelTrader.START_STATE

    def StopParallel(self):
        self.__continueRunning = False

    def Authenticate (self, namedAuthenticationPairs = dict):
        if self.IsAuthenticated() == False:
            authErrors = str

            for market in self.__portfolio:
                authErrors += market.AttemptAuthentication(namedAuthenticationPairs)

            return authErrors

        else:
            return ""

    def IsAuthenticated(self):
        for market in self.__portfolio:
            if market.IsAuthenticated == False:
                return False

        return True