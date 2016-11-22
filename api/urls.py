"""md_gate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [

    # # register a user
    # url(r'register/user',RegisterUserView.as_view({'post': 'create_user'})),
    # url(r'verify/user', RegisterUserView.as_view({'post': 'verify_user'})),
    #
    # # login and logout handlers
    # url(r'login/user/', LoginView.as_view({'post': 'login_user'})),
    # url(r'logout/user/', LogoutView.as_view({'post': 'logout_user'})),
    #
    # # product urls
    # url(r'create/product', ProductView.as_view({'post': 'create_prouct'})),
    # url(r'list/products', ProductView.as_view({'get': 'get_product_listing'})),
    # url(r'list/child/products/(?P<id>\d+)', ProductView.as_view({'get': 'get_child_products'})),
    # url(r'update/products', ProductView.as_view({'post': 'update_products'})),
    #
    # # gradeproduct
    # url(r'create/gradeproducts/(?P<product_pk>\d+)', GradeProductView.as_view({'post': 'create_grade_product'})),
    # url(r'list/gradeproducts', GradeProductView.as_view({'get': 'get_grade_product_listing'})),
    # url(r'update/gradeproduct/(?P<grade_product_pk>\d+)', GradeProductView.as_view({'post': 'update_grade_product'})),
    #
    #
    # # stock related functionality
    # url(r'create/stock_posting', StockView.as_view({'post': 'create_stock_posting'})),
    # url(r'get/stock_posting/listing/(?P<grade_product_id>\d+)/(?P<page_number>\d+)', StockView.as_view({'get': 'get_stock_list'})),
    # url(r'get/stock_posting/details/(?P<posting_pk>\d+)', StockView.as_view({'get': 'get_stock_detail'})),
    # url(r'update/stock_posting/(?P<posting_pk>\d+)', StockView.as_view({'post': 'update_stock_posting'})),
    # url(r'delete/stock_posting/(?P<posting_pk>\d+)', StockView.as_view({'delete': 'delete_stock_posting'})),
    #
    # # update order API
    # url(r'create/order', OrderView.as_view({'post': 'create_order'})),
    # url(r'update/order', OrderView.as_view({'post': 'update_order'})),
    # url(r'get/order/(?P<order_id>\d+)', OrderView.as_view({'get': 'get_order_status'})),
    #
    #
    # # UserProfile View
    # url(r'get/profile', UserProfileView.as_view({'get': 'get_userprofile'})),
    # url(r'update/profile', UserProfileView.as_view({'post': 'update_profile'})),

    # Search Company
    url(r'search_company', CompanySearchViewApi.as_view(), name="get_company_list"),
]
