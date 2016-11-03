from django.conf.urls import url
from web.views import Register, AddCompany, CheckCompany

urlpatterns = [
    url(r'^register/', Register),
    url(r'^add_company/', AddCompany),
    url(r'^check_company/', CheckCompany),
]
