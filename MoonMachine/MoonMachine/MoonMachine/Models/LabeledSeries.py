from pyalgotrade.bar import Bar
from pyalgotrade.dataseries.bards import BarDataSeries
from datetime import datetime
from MoonMachine.Models.LabeledBar import LabeledBar
from MoonMachine.Models.DatedLabel import DatedLabel
from collections.abc import MutableSequence
from overrides import overrides

class LabeledSeries(MutableSequence):

    def __init__(self, listOfNormalBars = BarDataSeries, listOfDatedLabels = list):
        """creates a series of LabeledBars by tagging bars with their closest labels"""
        super().__init__()
        self.UnderlyingBars = list()
        self.__combined = list()

        for currentLabeledBar in listOfNormalBars:
            labeledBarWip = LabeledBar(bar, list())
            barsDate = currentLabeledBar.getDateTime()
            datedLabelBeforeBar = object

            for datedLabel in listOfDatedLabels:
                datedLabel.Date.hour = 0
                datedLabel.Date.minute = 0
                datedLabel.Date.second = 0
                datedLabel.Date.microsecond = 0

                if datedLabel.Date <= barsDate: #assuming bar dates are ordered
                    labeledBarWip.Labels.append(datedLabel.Label)
                    self.__removePreviousOccurrencesOfLabel(datedLabel.Label)

            self.__combined.append(currentLabeledBar)
            self.UnderlayingLabels.append()

    def __removePreviousOccurrencesOfLabel(self, label = str):
        for removalBar in self.__combined:
            for comparisonLabel in removalBar.Labels:
                if comparisonLabel == label:
                    removalBar.Labels.remove(comparisonLabel)

    @overrides
    def append(self, value = LabeledBar):
        self.__combined.append(value)

    @overrides
    def clear(self):
        self.__combined.clear()

    @overrides
    def count(self, value):
        return self.__combined.count()

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
