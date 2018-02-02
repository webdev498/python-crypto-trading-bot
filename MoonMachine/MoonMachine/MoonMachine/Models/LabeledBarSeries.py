from pyalgotrade.dataseries.bards import BarDataSeries
from datetime import datetime
from MoonMachine.Models.LabeledBar import LabeledBar
from MoonMachine.Models.DatedLabel import DatedLabel
from collections.abc import MutableSequence
from overrides import overrides
from logging import Logger

class LabeledBarSeries(MutableSequence):
    def __init__(self, listOfNormalBars = list, listOfDatedLabels = list):
        """creates a series of LabeledBars by tagging bars with their closest labels. datetimes are automatically rounded down to the nearest day."""
        super().__init__()
        self.UnderlyingBars = BarDataSeries()
        self.__combined = list()
        self.__log = Logger(self.__class__)
        self.__log.info("constructing.")

        for currentBar in listOfNormalBars:
            self.UnderlyingBars.append(currentBar)
            labeledBarWip = LabeledBar(currentBar, [])
            barsDate = labeledBarWip.Bar.getDateTime()

            for datedLabel in listOfDatedLabels:
                #datetimes are immutable
                datedLabel.Date = datetime.replace(datedLabel.Date, hour = 0, minute = 0, second = 0, microsecond = 0) #im using a class method version in order to get at design time intellisense of a boxed datetime

                if datedLabel.Date <= barsDate: #assuming bar dates are ordered                    
                    self.__removePreviousOccurrencesOfLabel(datedLabel.Label) 
                    labeledBarWip.Labels.append(datedLabel.Label)

            self.__combined.append(labeledBarWip)         
            
        self.__log.info(self.__class__ + "constructed. ")

    def __removePreviousOccurrencesOfLabel(self, label = str):
        counter = 0

        for removalBar in self.__combined:
            for comparisonLabel in reverse(removalBar.Labels): #removing in reverse order ensures that the working index does not change
                if comparisonLabel == label:
                    counter += 1
                    removalBar.Labels.remove(comparisonLabel)

        self.__log.info("Duplicate labels of title '" + label + "' removed: " + str(counter))

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

    @overrides
    def __delitem__(self, index):
        self._combined.remove(index)

    @overrides 
    def __setitem__(self, index, value):
        self.__combined[index] = value

    def __len__(self):
        return len(self.__combined)

    def __getitem__(self, index):
        return self.__combined[index]