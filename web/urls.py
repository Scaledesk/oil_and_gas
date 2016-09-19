from django.conf.urls import url

from web.views import register

urlpatterns = [
    url(r'^register/', register),
]
