///<reference path="../Custom/RequestForgeryToken.js" />
///<reference path="../Custom/AuthFileUploader.js" />
///<reference path="../jquery-1.10.2.js" />
///<reference path="../knockout-3.4.2.min.js" />

function AuthorizedControlsViewModel()
{
    var self = this;
    SetupToken();
    self.FileUploader;

    var publicStuff = {
        ToggleButtonId: ko.observable("toggleButton"),
        FileBoxId: ko.observable("fileBox"),
        SubmitButtonId: ko.observable("submitButton"),
        
        ShouldDisplayControl: ko.pureComputed(function(){
            return self.FileUploader.IsAuthenticated();
        }),

        OnSubmit: function() {
            self.FileUploader.AttemptAuthenticationWithInput();
        },   
        
        OnToggle: function() {
            $.ajax ('ToggleOperations', {
                    data: { 
                    },
                    method: "POST"
                }
            )
            .success(function () {
                self.UpdateButtonLabelFromState();
            });
        },        
    };
    self.ToggleButton = document.getElementById(publicStuff.ToggleButtonId());
    self.FileUploader = new AuthFileUploader(publicStuff.FileBoxId());

    self.UpdateButtonLabelFromState = function() {
        self.ToggleButton.innerHTML = 'Loading...';

        $.getJSON('GetOperationsToggleIdentifier', {}, function (data, textStatus, jqXHR) {
            self.ToggleButton.innerHTML = String(data); //im using innerHTML because its the dom standard; textContent isnt universal yet
        });
    };
    self.UpdateButtonLabelFromState();
    return publicStuff;
}