"""
Definition of urls for MoonMachine.
"""

from django.conf.urls import url
from app.controllers.Pages import *
from app.controllers.AuthorizedControls import *
from app.controllers.TradeFeeds import TradeFeeds
from django.contrib.auth.decorators import login_required

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib.auth import views
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = [
    #PAGES
    

    url(r'^$',
        Index),

    url(r'^(?i)admin/authorizedcontrols', 
        AuthorizedControls),

    url(r'^(?i)admin', admin.site.urls,
        name = 'admin'),

    #INTERFACES

    #omitting the appended $ means it will match on a string which contains, not equals, the expression   
    url(r'^(?i)admin/toggleoperations', 
        ToggleOperations),

    url(r'^(?i)admin/getoperationstoggleidentifier',
        GetOperationsToggleIdentifier),

    url(r'^(?i)admin/authenticatewithfile',
        AuthenticateWithFile)

]
