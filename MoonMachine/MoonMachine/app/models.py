from django.db import models
from MoonMachine.SelectionOptions.ModelLimits import *
    
class Purchase(models.Model):
    SecurityType = models.CharField (max_length = PERCENTAGE_DIGITS)
    Amount = models.FloatField()
    Cost = models.FloatField()
    RateOfChange = models.DecimalField(max_digits = PERCENTAGE_DIGITS, decimal_places = PERCENTAGE_DIGITS)
    Confidence = models.DecimalField(max_digits = PERCENTAGE_DIGITS, decimal_places = PERCENTAGE_DIGITS)
    TimeOf = models.DateField()

    def FillFields(self, 
            securityType = models.CharField(), 
            amount = models.FloatField(), 
            cost = models.FloatField(), 
            rateOfChange = models.DecimalField(),
            confidence = models.DecimalField(),
            timeOf = models.DateField()):
        self.SecurityType = securityType
        self.Amount = amount
        self.Cost = cost
        self.RateOfChange = rateOfChange
        self.Confidence = confidence
        self.TimeOf = timeOf

class Sale(models.Model):
    SecurityType = models.CharField (max_length = PERCENTAGE_DIGITS)
    Amount = models.FloatField()
    ProfitPercent = models.FloatField()
    RateOfChange = models.FloatField()
    Confidence = models.DecimalField(max_digits = PERCENTAGE_DIGITS, decimal_places = PERCENTAGE_DIGITS)
         
    def FillFields(self, 
             securityType = models.FloatField(),
             amount = models.FloatField(),
             profitPercent = models.FloatField(),
             rateOfChange = models.FloatField(),
             confidence = models.DecimalField()):
        self.SecurityType = securityType
        self.Amount = amount
        self.ProfitPercent = profitPercent
        self.RateOfChange = rateOfChange
        self.Confidence = confidence
        self.MatchingBuyIn = matchingBuyIn
    