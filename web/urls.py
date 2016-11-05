from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^register/', Register),
    url(r'^search_and_claim_company/', SearchAndClaimCompany),
    url(r'^add_company/', AddCompany),
    url(r'^check_company/', CheckCompany),
    url(r'^search_company/', SearchCompany),
    url(r'^search_company2/', SearchCompany2),
    url(r'^test/', Test),
    url(r'^test2/', Test2),
    url(r'^test3', Test3),
]
