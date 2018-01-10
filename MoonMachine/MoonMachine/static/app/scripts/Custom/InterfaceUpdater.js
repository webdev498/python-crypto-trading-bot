///<reference path="../jquery-1.10.2.js" /> //signals to visual studio to reference this javascript file as a library

function InterfaceUpdater(toggleButtonId) {
    var self = this;
    self.publicStuff; //this better reflects the hoisting nature of javascript.
    self.buttonInterface = document.getElementById(toggleButtonId); 

    self.buttonInterface.onclick = function() {
        var currentAction = self.buttonInterface.innerHTML.toString();

        $.ajax ('ToggleOperations',
            {
                data: { 
                    'shouldOperate': currentAction 
                },
                method: "POST"
            }
        )
        .success(function () {
            self.publicStuff.UpdateButtonLabelFromState();
        });
    };

    self.publicStuff = {
        UpdateButtonLabelFromState: function() {
            self.buttonInterface.innerHTML = 'Loading...';

            $.getJSON('GetOperationsToggleIdentifier', {}, function (data, textStatus, jqXHR) {
                self.buttonInterface.innerHTML = String(data); //im using innerHTML because its the dom standard; textContent isnt universal yet
            });
        }
    };
    return self.publicStuff;
}