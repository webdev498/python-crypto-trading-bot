from pyalgotrade.bar import BasicBar
from datetime import datetime

class LabeledBar(object):
    def __init__(self, bar = BasicBar, labels = list):   
        self.Labels = labels  
        self.Bar = bar
        
