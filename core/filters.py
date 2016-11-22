import django_filters
from rest_framework import filters
from .models import *
from .serializers import CompanyModelSerializer


class CompanyModelFilter(filters.FilterSet):
    class Meta:
        model = CompanyModel
        fields = ['company_name']
