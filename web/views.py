from django.shortcuts import render, render_to_response, HttpResponse, Http404
from django.template import RequestContext
from pprint import pprint
# from django.utils import simplejson
import json as simplejson
from web.utils import CreateCompanyUtil,  CreateUserUtil, CreateCompanyUtil, CreateUserProfileUtil, CreateUserAndCompanyUtil, CreateUserAndClaimCompanyUtil
from web.forms import RegisterUserForm, AddCompanyForm, RegisterUserAndCompany

from core.models import *


def Register(request):
    # pass
    current_form = None
    context = None
    error = None
    is_registered = None

    if request.method == 'GET':
        current_form = RegisterUserAndCompany()

    if request.method == 'POST':
        current_form = RegisterUserAndCompany(request.POST)
        if current_form.is_valid():
            is_registered = CreateUserAndCompanyUtil(current_form.cleaned_data)
            if is_registered:
                return HttpResponse('User and Company are sucessfully created. Please wait for admin approval')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, "register.html", context={'form':current_form, 'error':error})

def SearchCompany(request):
    search_qs = CompanyModel.objects.filter(owner=UserProfile.objects.filter(user=User.objects.filter(is_superuser=True)))
    results = []
    for r in search_qs:
        results.append(r.company_name)
    # pprint(str(request.GET['callback']))
    # resp = request.GET['callback'] + '(' + simplejson.dumps(results) + ');'
    resp = simplejson.dumps(results)
    pprint(resp)
    return HttpResponse(resp, content_type='application/json')

def SearchAndClaimCompany(request):
    user_form = None
    if request.method == 'GET':
        user_form = RegisterUserForm()
        context = {'user_form':user_form}
    if request.method == 'POST':
        user_data_dict = request.POST
        company_name = user_data_dict.pop('company_name', None)
        user_form = RegisterUserForm(user_data_dict, company_name)
        if user_form.is_valid():
            if CreateUserAndClaimCompanyUtil(user_data_dict, company_name):
                return HttpResponse('User is Created and Company Claim is requested')
            else:
                HttpResponse('Internal Server Error')
        else:
            return Http404
    return render(request, 'search_and_claim_company.html', context)




def AddCompany(request):
    current_form = None
    context = None
    error = None

    if request.method == 'GET':
        current_form = AddCompanyForm()
        context = {'form':current_form}
        return render(request, "add_company.html", context=context)

    if request.method == 'POST':
        current_form =AddCompanyForm(request.POST)
        if current_form.is_valid():
            is_company_added = AddCompanyUtil(current_form.cleaned_data)
            if is_company_added == True:
                return HttpResponse('company added')
            else:
                HttpResponse('Server Error')
        else:
            context= {'form':current_form, 'error':error}
            error = current_form.errors.values()[0]
    return render(request, 'add_company.html',context=context)


def CheckCompany(request):
    if request.method == 'GET':
        current_form = AddCompanyForm()
        context = {'form':current_form}
        return render(request, 'check_company.html', context=context)
    if request.method == 'POST':
        pprint(request.POST)
        # pass
        return HttpResponse("abcaaa")




def SearchCompany2(request):
    search_qs = CompanyModel.objects.filter(owner=UserProfile.objects.filter(user=User.objects.filter(is_superuser=True)))
    results = []
    for r in search_qs:
        results.append(r.company_name)
    # pprint(str(request.GET['callback']))
    # resp = request.GET['callback'] + '(' + simplejson.dumps(results) + ');'
    resp = simplejson.dumps(results)
    pprint(resp)
    return HttpResponse(resp, content_type='application/json')


def Test(request):
    if request.method == 'GET':
        return render(request, 'test.html', None)

def Test2(request):
    if request.method == 'GET':
        return render(request, 'test2.html', None)

def Test3(request):
    if request.method == 'GET':
        return render(request, 'test3.html', None)