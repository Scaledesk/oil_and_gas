from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^login', Login),
    url(r'^logout', Logout),
    url(r'^create_user_and_claim_company/', CreateUserAndClaimCompany),
    url(r'^search_and_claim_company/', CreateUserAndClaimCompany),
    url(r'^create_user_and_company', CreateUserAndCompany),
    url(r'^search_company/', SearchCompany),

    #Free
    url(r'^free_fields', FreeFields),

    #Premium
    url(r'^free_fields', FreeFields),
    url(r'^gallery', Gallery),
    url(r'^basic_premium_fields', BasicPremiumFields),
    url(r'^brochure', Brochure),

    url(r'^video_link', VideoLink)



    #PremiumFields
    # url(r'^basic_premium_fields', BasicPremiumField),

]
