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

        AuthenticationOutcomes: ko.observableArray(),

        OnSubmit: function()
        {
            GetCurrentStatus()
                .then(function(data)
                {
                    if (data['status'] !== 'Idle')
                    {
                        answer = confirm('Are you sure you want to authenticate the bot while running?');

                        if (answer === false)
                        {
                            return;
                        }
                    }

                    self.FileUploader.AttemptAuthenticationWithInput(function (array)
                        {
                            publicStuff.AuthenticationOutcomes(array);
                        }
                    );
                });
        },         
        
        OnToggle: function()
        {      
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
        GetCurrentStatus()
            .then(function(status)
            {
                publicStuff.BotsStatus(JSON.stringify(status));
            });
    }

    function GetCurrentStatus()
    {
        return new Promise(function (resolve, reject)
        {
            $.getJSON('GetOperationsToggleIdentifier', {}, function OnGot(data, textStatus, jqXHR)
            {
                resolve(data);
            });
        });
    }
    return publicStuff;
}