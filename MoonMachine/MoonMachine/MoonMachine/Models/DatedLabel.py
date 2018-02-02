from datetime import datetime

class DatedLabel(object):
    """Date will be rounded down to the nearest hour."""
    def __init__(self, date = datetime, label = str):
        self.Date = date
        self.Label = str
