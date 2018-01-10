from pyalgotrade.bar import BasicBar
from datetime import datetime

class LabeledBar(object):
    def __init__(self, bar = BasicBar, labels = list):   
        self.Labels = labels  

        self.Bar = BasicBar(bar.getDateTime(),
                             bar.getOpen(),
                             bar.getHigh(),
                             bar.getLow(),
                             bar.getClose(),
                             bar.getVolume(),
                             bar.getAdjClose(),
                             bar.getFrequency(),
                             bar.getExtraColumns())
        
