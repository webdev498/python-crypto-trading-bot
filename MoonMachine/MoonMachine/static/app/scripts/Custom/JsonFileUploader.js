///<reference path="../jquery-1.10.2.js" />
///<reference path="../js_cookie.js" />

function JsonFileUploader()
{
    var self = this;
    self.statusLabel = document.getElementById ("authenticatedStatus");
    self.fileBox = document.getElementById("fileBox");

    self.AuthenticationWithFile = function(jsonString)
    {
        var csrfToken = Cookies.get('csrftoken');

        if (csrfToken === "") 
        {
            window.alert ('csrfToken is not present in cookies!');
            return;
        }

        var CsrfSafeMethod = function (method)            
        {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test (method));
        };

        $.ajaxSetup //django csrf only works out of the box with html form requests. in order to apply the csrf token to my post requests, I need to alter ajax setup here.
        (
            {
                beforeSend: function (xhr, settings)
                {
                    if(CsrfSafeMethod (settings.type) === false && 
                       this.crossDomain === false)
                    {
                        xhr.setRequestHeader ('X_CSRFToken', csrfToken);
                    }
                }
            }
        );

        $.ajax 
        (
            {
                url: "admin/authenticatewithfile",

                data: { 
                    'authenticationFile': jsonString
                },
                method: "POST",
                dataType: "json",                

                success: function(data)
                {
                    var authOutcome = Boolean (data);

                    if (authOutcome == true) 
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

    var publicStuff = {
        SubmitFile: function()
        {
            var file = fileBox.files[0];
            var reader = new FileReader();
            
            reader.onloadend = function() 
            {
                self.AuthenticationWithFile (reader.result);
            };
            reader.readAsText(file);
        }
    };
    return publicStuff;
};

var jsonUploader = JsonFileUploader();