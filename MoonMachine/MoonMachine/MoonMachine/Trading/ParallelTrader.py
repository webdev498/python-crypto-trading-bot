from threading import Thread
from MoonMachine.Trading.RestGateways.IndependentReserveContext import IndependentReserveContext
from MoonMachine.Trading.MarketManager import MarketManager
from MoonMachine.SelectionOptions.LabeledConstants import *
from threading import Lock
from logging import Logger

class ParallelTrader(object):
    IDLE_STATE = 'Idle'
    RUNNING_STATE = 'Running'    

    def __init__(self):
        Thread.__init__(self, name = "ParallelTrader")       
        
        self.__portfolio = [
            MarketManager(XBT_STRING, AUD_STRING, IndependentReserveContext()),
        ]
        
        self.__operation = ParallelTrader._Operation(self.__portfolio)
        self.__logger = Logger(self.__class__)
        self.__logger.info('initialised with ' + len(self.__portfolio) + ' markets.')
        
    def GetToggleSwitchesState(self):
        """Thread safe"""
        return self.__operation.ToggleSwitchesState

    def Start(self):
        """NOT THREAD SAFE"""
        if self.IsSufficientlyAuthenticated(): #blocks running a thread twice before Trader can change its ToggleSwitchesName
            self.__ToggleOperation(True)

    def Stop(self):
        """NOT THREAD SAFE"""
        self.__ToggleOperation(False)

    def __ToggleOperation(self, ShouldStart = bool):
        threadLock = Lock()

        with threadLock:
            if ShouldStart and self.__operation.is_alive() == False: #ensure that thread cannot be started twice
                self.__operation.start()

            elif self.__operation.is_alive():                    
                while self.__operation.is_alive():
                    pass

                self.__operation = ParallelTrader._Operation(self.__portfolio)

    def Authenticate (self, namedAuthenticationPairs = dict):
        """NOT THREAD SAFE"""
        self.__ToggleOperation(False)

        if self.IsSufficientlyAuthenticated() == False:
            authErrors = str()

            for market in self.__portfolio:
                authErrors += market.AttemptAuthentication(namedAuthenticationPairs)

            return authErrors

        else:
            return ""

    def IsSufficientlyAuthenticated(self):
        """NOT THREAD SAFE""" 
        for market in self.__portfolio:
            if market.IsAuthenticated == False:
                return False

        return True

    def GetAuthAppStatus(self):
        for market in self.__portfolio:
            return market.GetAuthAppStatus()

    class _Operation(Thread):  #single underscore notation signifies this is 
        def __init__(self, markets = list()):
            self.ToggleSwitchesState = ParallelTrader.IDLE_STATE
            self.__markets = markets

        def run(self):
            if self.ToggleSwitchesState == ParallelTrader.IDLE_STATE:
                self.ToggleSwitchesState = ParallelTrader.RUNNING_STATE      
                
                while self.ToggleSwitchesState == ParallelTrader.RUNNING_STATE:                          
                    for market in self.__markets:
                        market.Work()

                for market in self.__markets:
                    market.Dispose()

                self.ToggleSwitchesState = ParallelTrader.IDLE_STATE            
