from django.conf.urls import url

from .views import CompanyView

urlpatterns = [
    url(r'^register/', CompanyView.as_view()),
]