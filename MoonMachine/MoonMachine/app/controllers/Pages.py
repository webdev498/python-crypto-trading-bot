from django.http.request import HttpRequest
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.checks import check_user_model
from MoonMachine.SelectionOptions.MarketAction import MarketAction
from datetime import *
from decimal import Decimal


def AuthorizedControls(request = HttpRequest):
    response = None

    from MoonMachine.ModelsModule import Transaction
    #testTransaction = Transaction()
    #testTransaction.Fill(MarketAction.BUY, "", '', Decimal('1'), Decimal('1'), datetime(1, 1, 1), Decimal('1'), test = 'test')
    #testTransaction.save()    

    if request.user.is_authenticated:
        response = render(request, "app\AuthorizedControls.html")

    else:
        response = redirect('/admin')

    return response

def Index(request = HttpRequest):
    return render(request, "app\Index.html")

