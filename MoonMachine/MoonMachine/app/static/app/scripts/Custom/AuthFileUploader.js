///<reference path="../jquery-1.10.2.js" />
///<reference path="../knockout-3.4.2.min.js" />

function AuthFileUploader(fileBoxId)
{
    var self = this;
    self.AuthenticateWithJson;

    self.fileBox = document.getElementById(fileBoxId);
    
    function AuthenticateWithJson(jsonString) //declared functions are always available at any line in the class.
    {        
        $.ajax ("authenticatewithfile", {
            data: { 
                'authenticationFile': jsonString
            },
            method: "POST"
        })
        .success( function OnSuccess(data)
        {
            if (data === "") 
            {
                self.publicStuff.IsAuthenticated(true);
            }

            else {                
                self.publicStuff.IsAuthenticated(false);
                window.alert ("authentication failed: " + data);
            }
        })
        .error(function OnError(jqXHR, textStatus, errorThrown)
        {
            window.alert ("authentication failed: " + errorThrown);
        });
    };

    self.publicStuff = {
        AttemptAuthenticationWithInput: function()
        {
            var file = fileBox.files[0];
            var reader = new FileReader();
            
            reader.onloadend = function SubmitReadersText() 
            {
                var correctFormat = JSON.parse (reader.result);
                var correctString = JSON.stringify (correctFormat);
                AuthenticateWithJson (correctString);
            };

            if (file !== null)
            {
                reader.readAsText(file);
            }

            else if (self.publicStuff.IsAuthenticated())
            {
                AuthenticateWithJson(""); //covers up the fact that all authentication data must be erased when toggle button is clicked                
            }             

            else
            {
                window.alert("Input file not found.");
            }
        },
        IsAuthenticated: ko.observable(false)
    };
    return self.publicStuff;
}
