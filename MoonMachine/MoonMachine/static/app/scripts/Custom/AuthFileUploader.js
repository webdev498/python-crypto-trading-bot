///<reference path="../jquery-1.10.2.js" />

function AuthFileUploader(inputsId, resultLabelsId)
{
    var self = this;
    self.AuthenticateWithJson;
    self.publicStuff;

    self.fileBox = document.getElementById(inputsId);
    self.statusLabel = document.getElementById (resultLabelsId);
    
    AuthenticateWithJson = function(jsonString)
    {
        $.ajax 
        (
            {
                url: "authenticatewithfile",

                data: { 
                    'authenticationFile': jsonString
                },
                method: "POST",
                dataType: "json",                

                success: function(data)
                {
                    var authOutcome = Boolean (data);

                    if (authOutcome === true) 
                    {
                        statusLabel.innerText = "Authentication successful! Click for main page.";
                    }

                    else 
                    {
                        statusLabel.innerHTML = "";        
                    }
                }
            }
        );
    };

    self.publicStuff = {
        AttemptAuthenticationWithInput: function()
        {
            var file = fileBox.files[0];
            var reader = new FileReader();
            
            reader.onloadend = function() 
            {
                self.AuthenticateWithJson (reader.result);
            };
            reader.readAsText(file);
        }
    };
    return self.publicStuff;
}
