from django.views.decorators.http import require_POST
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json
from MoonMachine.Trading.ParallelTrader import ParallelTrader
from django.contrib.auth.decorators import login_required
from threading import Lock

Trader = ParallelTrader()
    
@login_required
@requires_csrf_token
@require_POST
def ToggleOperations (request = HttpRequest):
    global Trader #global must be defined everywhere that Trader is used so that it is not considered a local object      
    switchState = Trader.GetToggleSwitchesState()

    if switchState == ParallelTrader.IDLE_STATE:
        Trader.Start()                

    elif switchState == ParallelTrader.RUNNING_STATE:
        Trader.Stop(request)

    return HttpResponse()

@login_required
@requires_csrf_token
def GetBotsStatus(request = HttpRequest):
    global Trader
    return JsonResponse ({'status' : Trader.GetToggleSwitchesState()}, DjangoJSONEncoder, False)  

@login_required
@requires_csrf_token
@require_POST
def AuthenticateWithFile (request = HttpRequest):
    global Trader
    inputText = request.POST.get ('authenticationFile')
    fileAsJson = json.loads (inputText)
    authErrors = Trader.Authenticate (fileAsJson)
    return JsonResponse(authErrors)