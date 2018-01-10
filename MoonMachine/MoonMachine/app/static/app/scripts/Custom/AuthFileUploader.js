///<reference path="../jquery-1.10.2.js" />
///<reference path="../knockout-3.4.2.min.js" />

function AuthFileUploader(fileBoxId)
{
    var self = this;
    self.AuthenticateWithJson;
    var publicStuff;

    self.fileBox = document.getElementById(fileBoxId);
    
    self.AuthenticateWithJson = function(jsonString)
    {        
        $.ajax ("authenticatewithfile", {
            data: { 
                'authenticationFile': jsonString
            },
            method: "POST"
        })
        .success( function(data)
        {
            if (data === "") 
            {
                publicStuff.IsAuthenticated(true);
                window.alert("Authentication successful!");
            }

            else {
                publicStuff.IsAuthenticated(false);
            }
        })
        .error(function(jqXHR, textStatus, errorThrown)
        {
            window.alert ("request broke.");
        });
    };

    publicStuff = {
        AttemptAuthenticationWithInput: function()
        {
            var file = fileBox.files[0];
            var reader = new FileReader();
            
            reader.onloadend = function() 
            {
                var correctFormat = JSON.parse (reader.result);
                var correctString = JSON.stringify (correctFormat);
                self.AuthenticateWithJson (correctString);
            };
            reader.readAsText(file);
        },
        IsAuthenticated: ko.observable()
    };
    return publicStuff;
}
