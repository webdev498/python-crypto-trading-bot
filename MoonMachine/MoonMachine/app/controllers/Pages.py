from django.http.request import HttpRequest
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.checks import check_user_model

class Pages(object):
    """description of class"""
    def __init__(self):
        pass

    def AuthorizedControls(request):
        response = None

        if request.user.is_authenticated:
            response = render_to_response("app\AuthorizedControls.html")

        else:
            response = redirect('/admin')

        return response


