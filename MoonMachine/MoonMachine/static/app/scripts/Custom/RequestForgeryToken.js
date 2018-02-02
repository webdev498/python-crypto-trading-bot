///<reference path="../js_cookie.js" />

function SetupCsrfToken()
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
                if (CsrfSafeMethod (settings.type) && 
                    this.crossDomain === false)
                {
                    window.alert('csrf token set ');
                    xhr.setRequestHeader ('X-CSRFToken', csrfToken); //fixed bug where string was not in the right forma
                }
            }
        }
    );
}