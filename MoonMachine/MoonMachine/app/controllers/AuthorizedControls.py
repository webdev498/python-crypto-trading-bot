from manage import Trader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from threading import Lock
import json
from MoonMachine.Trading.ParallelTrader import ParallelTrader
from django.contrib.auth.decorators import login_required

class AuthorizedControls(object):
    """description of class"""
    def __init__(self):
        pass
    
    @login_required
    @requires_csrf_token
    @require_POST
    def ToggleOperations (request = HttpRequest):
        global Trader #global must be defined everywhere that Trader is used so that it is not considered a local object
       
        if Trader.ToggleSwitchesState == ParallelTrader.START_STATE and Trader.is_alive() == False and Trader.IsAuthenticated(): #blocks running a thread twice before Trader can change its ToggleSwitchesName
            Trader.start()                

        elif Trader.ToggleSwitchesState == ParallelTrader.STOP_STATE and Trader.is_alive():
            self.__ReinstanceThreadWithLock()
    
        return HttpResponse()

    @login_required
    def GetOperationsToggleIdentifier(request = HttpRequest):
        global Trader
        return JsonResponse (Trader.ToggleSwitchesState, DjangoJSONEncoder, False) #setting the safe param to false always with non dictionary words? /shrug       

    @login_required
    @requires_csrf_token
    @require_POST
    def AuthenticateWithFile (request = HttpRequest):
        global Trader
        inputText = request.POST.get ('authenticationFile')
        fileAsJson = json.loads (inputText)
        authErrors = Trader.Authenticate (fileAsJson)
        return HttpResponse(authErrors)

    @login_required
    def __ReinstanceThreadWithLock(self):
            global Trader
            stopLock = Lock()

            with stopLock: #Trader is not thread safe and can throw if invoked while being Reinstanced
                Trader.StopParallel()
                
                while Trader.is_alive():
                    pass
                
                Trader = ParallelTrader()

