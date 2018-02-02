from django.http.request import HttpRequest
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.checks import check_user_model


def AuthorizedControls(request = HttpRequest()):
    response = None

    if request.user.is_authenticated:
        response = render_to_response("app\AuthorizedControls.html")

    else:
        response = redirect('/admin')

    return response


