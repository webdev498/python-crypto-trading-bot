from threading import Thread
from django.http.request import HttpRequest
from MoonMachine.Trading.MarketManager import MarketManager
from MoonMachine.SelectionOptions.LabeledConstants import *
from threading import Lock
from logging import Logger, getLogger
from ccxt import independentreserve
from MoonMachine.Trading.RestGateways.IndependentReserveWrapper import IndependentReserveWrapper

class ParallelTrader(object):
    IDLE_STATE = 'Idle'
    RUNNING_STATE = 'Running'    

    def __init__(self):             
        self.__portfolio = [
            MarketManager(AUD_STRING, XBT_STRING, IndependentReserveWrapper()),
        ]
        self.__operation = ParallelTrader._Operation(self.__portfolio)
        self.__log = Logger(str(self.__class__))
        self.__log.info('initialised with ' + str(len(self.__portfolio)) + ' markets.')
        
    def GetToggleSwitchesState(self):
        self.__log.info('returning a switch state of: ' + str(self.__operation.ToggleSwitchesState))
        return self.__operation.ToggleSwitchesState

    def Start(self):
        if self.IsSufficientlyAuthenticated(): #blocks running a thread twice before Trader can change its ToggleSwitchesName
            self.__log.info('starting parallel trader.')
            self.__ToggleOperation(True)

    def Stop(self, request = HttpRequest):
        self.__log.info('stopping parallel trader.')
        
        for manager in self.__portfolio:
            manager.SetRequestObject(request)

        self.__ToggleOperation(False)

    def __ToggleOperation(self, ShouldStart = bool):
        threadLock = Lock()

        with threadLock:
            if ShouldStart and self.__operation.is_alive() == False: #ensure that thread cannot be started twice
                self.__log.info('toggling operation to state: ' + str(ShouldStart))
                self.__operation.start()

            elif self.__operation.is_alive():
                self.__log.info('toggling operation to state: ' + str(ShouldStart))
                self.__operation.ToggleSwitchesState = ParallelTrader.IDLE_STATE

                while self.__operation.is_alive():
                    pass

                self.__log.info('parallel trader stopped.')
                self.__operation = ParallelTrader._Operation(self.__portfolio)

    def Authenticate (self, namedAuthenticationPairs = dict):
        self.__log.info('authenticating parallel trader.')        
        originalState = self.__operation.isAlive()
        self.__ToggleOperation(False)
        authOutcomes = dict()
        self.__log.info('authenticating ' + str(len(self.__portfolio)) + ' market managers.')

        for manager in self.__portfolio:
            authOutcomes[manager.GetManagerName()] = manager.AttemptAuthentication(namedAuthenticationPairs)
      
        self.__log.info('toggling operations back to the ' + str(originalState) + ' state.')
        self.__ToggleOperation(originalState)
        return authOutcomes

    def IsSufficientlyAuthenticated(self):
        self.__log.info('checking trader is sufficiently authenticated...')
        for market in self.__portfolio:
            if market.IsAuthenticated() == False:
                self.__log.info('its not.')
                return False
        self.__log.info('it is.')
        return True

    class _Operation(Thread):  #single underscore notation signifies this is 
        def __init__(self, markets = list):
            self.__log = getLogger(str(self.__class__))            
            self.ToggleSwitchesState = ParallelTrader.IDLE_STATE
            self.__markets = markets
            super().__init__()
            self.__log.info('created new operation.')

        def run(self):
            if self.ToggleSwitchesState == ParallelTrader.IDLE_STATE:
                self.ToggleSwitchesState = ParallelTrader.RUNNING_STATE      
                
                while self.ToggleSwitchesState == ParallelTrader.RUNNING_STATE:      
                    for market in self.__markets:
                        market.Work()

                for market in self.__markets:
                    market.Dispose()

                self.ToggleSwitchesState = ParallelTrader.IDLE_STATE


        