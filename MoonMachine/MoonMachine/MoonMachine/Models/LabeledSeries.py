from pyalgotrade.bar import Bar
from datetime import datetime
from MoonMachine.Models.LabeledBar import LabeledBar
from MoonMachine.Models.DatedLabel import DatedLabel
from collections.abc import MutableSequence
from overrides import overrides

class LabeledSeries(MutableSequence):

    def __init__(self, listOfNormalBars = list, listOfDatedLabels = list):
        """creates a series of LabeledBars by tagging bars with their closest labels"""
        super().__init__()
        self.__items = list()

        for bar in listOfNormalBars:
            labeledBarWip = LabeledBar(bar, list())
            barsDate = bar.getDateTime()
            datedLabelBeforeBar = object
                     
            for datedLabel in listOfDatedLabels:
                datedLabel.Date.hour = 0
                datedLabel.Date.minute = 0
                datedLabel.Date.second = 0
                datedLabel.Date.microsecond = 0

                if datedLabel.Date <= barsDate:
                    labeledBarWip.Labels.append(datedLabel.Label)
                    self.__removePreviousOccurrencesOfLabel(datedLabel.Label)

            self.__items.append(currentLabeledBar)

    def __removePreviousOccurrencesOfLabel(self, label = str):
        for removalBar in self.__items:
            for comparisonLabel in removalBar.Labels:
                if comparisonLabel == label:
                    removalBar.Labels.remove(comparisonLabel)

    @overrides
    def append(self, value = LabeledBar):
        self.__items.append(value)

    @overrides
    def clear(self):
        self.__items.clear()

    @overrides
    def count(self, value):
        return self.__items.count()

    @overrides
    def extend(self, values = list):
        self.__items.extend(list)

    @overrides
    def index(self, value, start = 0, stop = None):
        return self.__items.index(value, start, stop)

    @overrides
    def insert(self, index, value):
        self.__items.insert(index, value)

    @overrides
    def pop(self, index):
        return self.__items.pop(index)

    @overrides
    def remove(self, value):
        self.__items.remove(value)

    @overrides
    def reverse(self):
        self.__items.reverse()