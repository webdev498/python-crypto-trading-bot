from MoonMachine.Models.LabeledSeries import LabeledSeries
from pyalgotrade.technical.rsi import rsi
from pyalgotrade.strategy import BaseStrategy

class StaticStrategy(BaseStrategy):
    """description of class"""
    def __init__(self):
        self.__shortTermIndicators = []
        self.__LongTermIndicators = []

    def DetermineDecision(self, data = LabeledSeries):
        pass