from datetime import datetime

class DatedLabel(object):
    """Date will be rounded down to the nearest hour."""
    def __init__(self, date = datetime, label = str):
        date.minute = 0
        date.second = 0
        date.microsecond = 0
        self.Date = date
        self.Label = label
