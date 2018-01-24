from MoonMachine.Trading.Analysis.LibraryIndicators import LibraryIndicators
from MoonMachine.Trading.Analysis.MemeTriangleEstimator import MemeTriangleEstimator
from pyalgotrade.dataseries import DataSeries
from MoonMachine.Trading.Strategy import LearningStrategy, StaticStrategy

class ExecutiveAnalyzer(object):
    """description of class"""
    def __init__(self):
        self.__libraryIndicators = LibraryIndicators()
        self.__memeTriangleEstimator = MemeTriangleEstimator()
        self.__staticStrat = new StaticStrategy()

    def ForumlateDecision(self):
        pass
