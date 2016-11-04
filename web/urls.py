from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^register/', Register),
    url(r'^add_company/', AddCompany),
    url(r'^check_company/', CheckCompany),
    url(r'^search_company/', SearchCompany),
    url(r'^test/', Test),
    url(r'^test2/', Test2),
]
