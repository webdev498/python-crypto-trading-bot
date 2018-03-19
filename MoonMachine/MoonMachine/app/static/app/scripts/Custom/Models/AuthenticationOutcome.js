///<reference path="../../knockout-3.4.2.min.js" />

function AuthenticationOutcome(marketManagerName, outcome)
{
    return {
        MarketManagerName: ko.observable(marketManagerName),
        Outcome: ko.observable(outcome),
    };
}