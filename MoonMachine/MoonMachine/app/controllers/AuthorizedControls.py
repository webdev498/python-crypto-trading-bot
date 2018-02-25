from manage import Trader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json
from MoonMachine.Trading.ParallelTrader import ParallelTrader
from django.contrib.auth.decorators import login_required
from threading import Lock

botLock = Lock()
    
@login_required
@requires_csrf_token
@require_POST
def ToggleOperations (request = HttpRequest()):
    global Trader #global must be defined everywhere that Trader is used so that it is not considered a local object      
    global botLock
    switchState = Trader.GetToggleSwitchesState()

    with botLock:
        if switchState == ParallelTrader.IDLE_STATE:
            Trader.Start()                

        elif switchState == ParallelTrader.RUNNING_STATE:
            Trader.Stop()
    
    return HttpResponse()

@login_required
@requires_csrf_token
def GetOperationsToggleIdentifier(request = HttpRequest()):
    global Trader
    return JsonResponse (Trader.GetToggleSwitchesState(), DjangoJSONEncoder, False) #setting the safe param to false always with non dictionary words? /shrug       

@login_required
@requires_csrf_token
@require_POST
def AuthenticateWithFile (request = HttpRequest()):
    global Trader
    inputText = request.POST.get ('authenticationFile')
    fileAsJson = json.loads (inputText)
    authErrors = str()
    authErrors = Trader.Authenticate (fileAsJson)
    return HttpResponse(authErrors)