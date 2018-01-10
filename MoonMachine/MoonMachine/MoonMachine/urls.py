"""
Definition of urls for MoonMachine.
"""

from django.conf.urls import url
from app.controllers.Pages import Pages
from app.controllers.AuthorizedControls import AuthorizedControls
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
        TemplateView.as_view(template_name="app/index.html")),

    url(r'^(?i)admin/authorizedcontrols', 
        Pages.AuthorizedControls),

    url(r'^(?i)admin', include(admin.site.urls),
        name = 'admin'),

    #INTERFACES

    #omitting the appended $ means it will match on a string which contains, not equals, the expression   
    url(r'^(?i)admin/toggleoperations', 
        AuthorizedControls.ToggleOperations),

    url(r'^(?i)admin/getoperationstoggleidentifier',
        AuthorizedControls.GetOperationsToggleIdentifier),

    url(r'^(?i)admin/authenticatewithfile',
        AuthorizedControls.AuthenticateWithFile),

]
