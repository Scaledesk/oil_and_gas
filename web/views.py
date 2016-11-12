from django.shortcuts import render, render_to_response, HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pprint import pprint
# from django.utils import simplejson
import json as simplejson
# from web.utils import CreateCompanyUtil,  CreateUserUtil, CreateCompanyUtil, CreateUserProfileUtil, CreateUserAndCompanyUtil, CreateUserAndClaimCompanyUtil,  CreateUserAndUserProfileUtil# from web.forms import CreateUserForm, CreateCompanyForm, CreateUserAndCompanyForm
from web.utils import *
from web.forms import *
from core.models import *


def Landing(request):
    context=None
    return render(request, 'landing.html', context=context)

@login_required
def Dashboard(request):
    context=None
    return render(request, 'dashboard.html', context=context)
@login_required
def AccountSetting(request):
    pass

def Login(request):
    if request.method == 'GET':
        next = request.GET.get('next', '/')
    if request.method == "POST":
        next = request.GET.get('next', '/')
        user_email = request.POST['user_email']
        password = request.POST['password']
        user = authenticate(username=user_email, password=password)        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            error = 'Incorrect Email or Password'
            return render(request, 'login.html',
                          context={'error': error, 'next':next})
    else:
        return render(request, "login.html", {'next': next})

@login_required
def Logout(request):
    logout(request)
    LogoutMessage="Logout Successful"
    return HttpResponse('logout sucessful')
    return render(request, 'login.html',
                  context={'message':LogoutMessage})

def SearchCompany(request):
    search_qs = CompanyModel.objects.filter(is_claimed=False, is_approved=True)
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
#                 return HttpResponse('company added')import CreateUserForm, CreateCompanyForm, CreateUserAndCompanyForm
#             else:
#                 HttpResponse('Server Error')
#         else:
#             context= {'form':current_form, 'error':error}
#             error = current_form.errors.values()[0]
#     return render(request, 'add_company.html',context=context)

@login_required
def FreeField(request):
    current_form = None
    error = None
    if request.method == 'GET':
        current_form = FreeFieldForm()
    if request.method == 'POST':
        current_form = FreeFieldForm(request.POST)
        if current_form.is_valid():
            if CreateFreeFieldUtil(current_form.cleaned_data, request.user):
                return HttpResponse('data has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]            
    return render(request, 'free/free_field.html', context = {'form':current_form, 'error':error})




@login_required
def BasicPremiumField(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')
    
    current_form = None
    error = None
    if request.method == 'GET':
        current_form = BasicPremiumFieldForm()
    if request.method == 'POST':
        current_form = BasicPremiumFieldForm(request.POST, request.FILES)
        if current_form.is_valid():
            if CreateBasicPremiumFieldUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Basic Premium Fields Been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/basic_premium_field.html', context = {'form':current_form, 'error':error})

@login_required
def Gallery(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')

    current_form = None
    error = None
    if request.method == 'GET':
        current_form = GalleryForm()
    if request.method == 'POST':
        current_form = GalleryForm(request.POST, request.FILES)
        if current_form.is_valid():
            if CreateGalleryUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Gallery Image has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/gallery.html', context = {'form':current_form, 'error':error})

@login_required
def Brochure(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')

    current_form = None
    error = None
    if request.method == 'GET':
        current_form = BrochureForm()
    if request.method == 'POST':
        current_form = BrochureForm(request.POST, request.FILES)
        if current_form.is_valid():
            if CreateBrochureUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Brochure has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/brochure.html', context = {'form':current_form, 'error':error})


@login_required
def VideoLink(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')

    current_form = None
    error = None
    if request.method == 'GET':
        current_form = VideoLinkForm()
    if request.method == 'POST':
        current_form = VideoLinkForm(request.POST)
        if current_form.is_valid():
            if CreateVideoLinkUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Video Link has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/video_link.html', context = {'form':current_form, 'error':error})

#KeyAlliance to be defined here

@login_required
def Location(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')

    current_form = None
    error = None
    if request.method == 'GET':
        current_form = LocationForm()
    if request.method == 'POST':
        current_form = LocationForm(request.POST)
        if current_form.is_valid():
            if CreateLocationUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Location has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/location.html', context = {'form':current_form, 'error':error})

@login_required
def Certification(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')

    current_form = None
    error = None
    if request.method == 'GET':
        current_form = CertificationForm()
    if request.method == 'POST':
        current_form = CertificationForm(request.POST, request.FILES)
        if current_form.is_valid():
            if CreateCertificationUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Certification has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/certification.html', context = {'form':current_form, 'error':error})

@login_required
def SocialLink(request):
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')
        
    current_form = None
    error = None
    if request.method == 'GET':
        current_form = SocialLinkForm()
    if request.method == 'POST':
        current_form = SocialLinkForm(request.POST, request.FILES)
        if current_form.is_valid():
            if CreateSocialLinkUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Social Links has been saved')
            else:
                return Http404
        else:
            error = current_form.errors.values()[0]
    return render(request, 'premium/social_link.html', context = {'form':current_form, 'error':error})


@login_required
def Publication(request):
    error = None
    current_form = None
    if request.method == 'GET':
        current_form = PublicationForm()
    if request.method == 'POST':
        current_form = PublicationForm(request.POST)
        if current_form.is_valid():
            if PublicationUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Publication has been saved')
            else:
                return HttpResponse('server error')
        else:
            error = pf.errors.values()[0]
    return render(request, 'super_premium/publication.html', context={'form':current_form, 'error':error})


def Test(request):
    if request.method == 'GET':
        return render(request, 'test.html', context=None)
    if request.method=='POST':
        pass