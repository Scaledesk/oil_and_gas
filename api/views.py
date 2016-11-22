# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from rest_framework import status
# # from core.utils import authenticate_user, generic_key_validator, registered_userregister_user, \
#                         # create_stock_posting
# from rest_framework.authtoken.models import Token
# # from core.app_settings import LOGIN, REGISTER, RECORDS_PER_PAGE, CREATE_STOCK, \
# #     SERIALIZABLE_VALUE
#
# from core.models import *
#
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.renderers import JSONRenderer
# from rest_framework.permissions import IsAuthenticated
# from django.views.generic import generics


from rest_framework import filters
from rest_framework import generics
from core.models import *
from core.serializers import *
from core.filters import CompanyModelFilter


# class BaseAPI(viewsets.ViewSet):
#     """
#     Base class for all the APIViews
#     """
#     pass

class CompanySearchViewApi(generics.ListAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanyModelSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    filter_class=CompanyModelFilter
    search_fields = ('company_name',)
