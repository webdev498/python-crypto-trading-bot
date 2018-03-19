///<reference path="../jquery-1.10.2.js" />
///<reference path="../knockout-3.4.2.min.js" />
///<reference path="Models/AuthenticationOutcome.js" />

function AuthFileUploader(fileBoxId)
{
    var self = this;
    self.fileBox = document.getElementById(fileBoxId);
    
    self.UploadAuthFile = function(jsonString, onSuccessCallBack, onErrorCallback) //declared functions are always available at any line in the class.
    {        
        $.ajax ("authenticatewithfile", {
            data: { 
                'authenticationFile': jsonString
            },
            method: "POST"
        })
        .success(function (data)
        {
            keys = Object.keys(data);

            if (keys.length > 0) 
            {
                frontEndFormatOutcomes = [];

                for (var i = 0; i < keys.length; i++)
                {
                    formattedOutcome = (data[keys[i]] === "") ? true : false;
                    frontEndFormatOutcomes.push(new AuthenticationOutcome(keys[i], formattedOutcome));
                }
                publicStuff.IsAuthenticated(true);                
                onSuccessCallBack(frontEndFormatOutcomes);
            }

            else {                
                publicStuff.IsAuthenticated(false);
                window.alert ("authentication failed.");
            }
        })
        .error(function OnError(jqXHR, textStatus, errorThrown)
        {
            onErrorCallback(errorThrown);
            window.alert ("authentication failed: " + errorThrown);
        });
    };

    var publicStuff = {
        AttemptAuthenticationWithInput: function(onSuccessCallBack, onErrorCallback)
        {
            var file = fileBox.files[0];
            var reader = new FileReader();
            
            reader.onloadend = function SubmitReadersText() 
            {
                try
                {
                    var correctFormat = JSON.parse (reader.result);
                    var correctString = JSON.stringify(correctFormat);
                    self.UploadAuthFile(correctString, onSuccessCallBack, onErrorCallback);
                }

                catch (e)
                {
                    alert('Files text could not be turned into json')
                }                
            };

            if (file !== null)
            {
                reader.readAsText(file);
            }

            else
            {
                window.alert("Input file not found.");
            }
        },
        IsAuthenticated: ko.observable(false)
    };
    return publicStuff;
};
