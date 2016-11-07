from django.shortcuts import render, render_to_response, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pprint import pprint
# from django.utils import simplejson
import json as simplejson
from web.utils import CreateCompanyUtil,  CreateUserUtil, CreateCompanyUtil, CreateUserProfileUtil, CreateUserAndCompanyUtil, CreateUserAndClaimCompanyUtil,  CreateUserAndUserProfileUtil
from web.forms import CreateUserForm, CreateCompanyForm, CreateUserAndCompanyForm

from core.models import *



def Login(request):
    # return HttpResponse('chal rha hai')
    next = request.GET.get('next', '/')
    if request.method == "POST":
        user_email = request.POST['user_email']
        password = request.POST['password']
        user = authenticate(username=user_email, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponse('Login sucessfull') #remove this once proper page is designeds
            return HttpResponseRedirect(next)
        else:
            error = 'Incorrect Email or Password'
            return render(request, 'login.html',
                          context={'error': error})
    else:
        return render(request, "login.html", {'redirect_to': next})

@login_required
def Logout(request):
    logout(request)
    LogoutMessage="Logout Successful"
    return render(request, 'login.html',
                  context={'message':LogoutMessage})
    

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

def CreateUserAndClaimCompany(request):
    user_form = None
    if request.method == 'GET':
        user_form = CreateUserForm()
        context = {'user_form':user_form}
    if request.method == 'POST':
        user_data_dict = request.POST
        company_name = request.POST['company_name']
        user_data_dict.pop('company_name', None)
        # return HttpResponse(company_name)
        # obj = CompanyModel.objects.filter(company_name=company_name)
        user_form = CreateUserForm(user_data_dict)
        if user_form.is_valid():
            if CreateUserAndClaimCompanyUtil(user_data_dict, company_name):
                return HttpResponse('User is Created and Company Claim is requested')
            else:
                HttpResponse('Internal Server Error')
        else:
            return Http404
    return render(request, 'create_user_and_claim_company.html', context)


def CreateUserAndCompany(request):
    current_form = None
    context = None
    error = None
    is_registered = None

    if request.method == 'GET':
        current_form = CreateUserAndCompanyForm()

    if request.method == 'POST':
        current_form = CreateUserAndCompanyForm(request.POST)
        if current_form.is_valid():
            is_registered = CreateUserAndCompanyUtil(current_form.cleaned_data)
            if is_registered:
                return HttpResponse('User and Company are sucessfully created. Please wait for admin approval')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, "create_user_and_company.html", context={'form':current_form, 'error':error})

# def AddCompany(request):
#     current_form = None
#     context = None
#     error = None

#     if request.method == 'GET':
#         current_form = AddCompanyForm()
#         context = {'form':current_form}
#         return render(request, "add_company.html", context=context)

#     if request.method == 'POST':
#         current_form =AddCompanyForm(request.POST)
#         if current_form.is_valid():
#             is_company_added = AddCompanyUtil(current_form.cleaned_data)
#             if is_company_added == True:
#                 return HttpResponse('company added')
#             else:
#                 HttpResponse('Server Error')
#         else:
#             context= {'form':current_form, 'error':error}
#             error = current_form.errors.values()[0]
#     return render(request, 'add_company.html',context=context)