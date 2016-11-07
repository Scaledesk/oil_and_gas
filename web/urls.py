from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^login', Login),
    url(r'^logout', Logout),
    url(r'^create_user_and_claim_company/', CreateUserAndClaimCompany),
    url(r'^search_and_claim_company/', CreateUserAndClaimCompany),
    url(r'^create_user_and_company', CreateUserAndCompany),
    url(r'^search_company/', SearchCompany),
]
