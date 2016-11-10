from django.conf.urls import url
from web.views import *

urlpatterns = [
    url(r'^login', Login),
    url(r'^logout', Logout),
    url(r'^create_user_and_claim_company/', CreateUserAndClaimCompany),
    url(r'^create_user_and_company', CreateUserAndCompany),
    url(r'^search_company/', SearchCompany),

    #Free
    url(r'^free_field', FreeField),

    #Premium
    url(r'^gallery', Gallery),
    url(r'^basic_premium_field', BasicPremiumField),
    url(r'^brochure', Brochure),

    url(r'^video_link', VideoLink),
    url(r'^location', Location),
    url(r'^certification', Certification),
    url(r'^social_link', SocialLink),



    #PremiumFields
    # url(r'^basic_premium_fields', BasicPremiumField),

]
