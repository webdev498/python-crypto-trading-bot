///<reference path="../Custom/AuthFileUploader.js" />
///<reference path="../jquery-1.10.2.js" />
///<reference path="../knockout-3.4.2.min.js" />

function AuthorizedControlsViewModel()
{
    var self = this;      
    self.FileUploader = new AuthFileUploader("fileBox");

    var publicStuff = {
        ShouldDisplayControl: ko.pureComputed(function()
        {
            ApplyCurrentStatus();
            return self.FileUploader.IsAuthenticated(); 
        }, self),

        OnSubmit: function()
        {
            self.FileUploader.AttemptAuthenticationWithInput();
        },   
        
        OnToggle: function() {            
            $.ajax ('ToggleOperations', {
                    data: { 
                    },
                    method: "POST"
                }
            )
            .success(function()
            {
                ApplyCurrentStatus();
            });
        },

        BotsStatus: ko.observable()
    };

    function ApplyCurrentStatus()
    {
        $.getJSON('GetOperationsToggleIdentifier', {}, function OnGot(data, textStatus, jqXHR)
        {
            publicStuff.BotsStatus(JSON.stringify(data));
        });
    }
    return publicStuff;
}