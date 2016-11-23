from django.shortcuts import render, render_to_response, HttpResponse, Http404, redirect
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
    """Landing page"""
    context={}
    if request.GET.get('status') == "logout":
        context['message'] = ("Logout Successful")
    return render(request, 'landing.html', context=context)

@login_required
def Dashboard(request):
    """Dashboard Page"""
    context={}
    if request.GET.get('status') == 'login':
        context['message'] = "Login Sucessful"
    return render(request, 'dashboard.html', context=context)

@login_required
def AccountSetting(request):
    """view to render account setting apge"""
    pass

def Login(request):
    """view to handle incoming login request"""
    if request.method == 'GET':
        next = request.GET.get('next', '/')
    if request.method == "POST":
        next = request.GET.get('next', '/')
        user_email = request.POST['user_email']
        password = request.POST['password']
        user = authenticate(username=user_email, password=password)
        if user is not None:
            login(request, user)
            if next == '/':
                return redirect('/web/dashboard/?status=login')
            return HttpResponseRedirect(next)
        else:
            error = 'Incorrect Email or Password'
            return render(request, 'login.html',
                          context={'error': error, 'next':next})
    else:
        return render(request, "login.html", {'next': next})

def Logout(request):
    """view to handle the incoming logout requst"""
    logout(request)
    return redirect('/web/landing/?status=logout')
    LogoutMessage="Logout Successful"
    return render(request, 'landing.html',
                  context={'message':LogoutMessage})

def GetCompany(request):
    """view to handle the ajax request when user search for the company to claim"""
    search_qs = CompanyModel.objects.filter(is_claimed=False, is_approved=True)
    results = []
    for r in search_qs:
        results.append(r.company_name)
    resp = simplejson.dumps(results)
    return HttpResponse(resp, content_type='application/json')

def CreateUserAndClaimCompany(request):
    """view to handle the request to create user and to save a company claim request"""
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
    """veiw to create new usear and new company when company do not exist in database"""
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
    """view to handle the premium fields"""
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
    """ view to handle the gallery images """
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
    """ view to save the company brochure """
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
    """view to save the video links """
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

def SearchAlliance(request):
    """ view to render companies in the database on ajax request when user search for companies to form alliances """
    search_qs = CompanyModel.objects.filter(is_approved=True)
    results = []
    for r in search_qs:
        results.append(r.company_name)
    resp = simplejson.dumps(results)
    return HttpResponse(resp, content_type='application/json')

@login_required
def Alliance(request):
    """view to save the company's alliance to other company already in the database """
    if not IsPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')
    if request.method == 'POST':
        company_name = request.POST['company_name']
        if KeyAlliance.objects.filter(key_alliance=CompanyModel.objects.filter(company_name=company_name)):
            return HttpResponse('Alliance is already saved in the database')
        if CompanyModel.objects.get(owner=request.user).company_name==company_name:
            return HttpResponse('You can no form alliance with your own company')
        else:
            if CreateKeyAllianceUtil(company_name, request.user):
                return HttpResponse('Alliance has been saved in the database')
            else:
                return HttpResponse('Server Error')
    return render(request, 'premium/alliance.html', context=None)

@login_required
def Location(request):
    """view to save the location of company"""
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
    """" view to save the certification of the company """
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
    """view to save the social media links of the company"""
    if not IsSuperPremium(request.user):
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
    """view to save the published articles of the company"""
    if not IsSuperPremium(request.user):
        return HttpResponse('This will require premium subscription or super-premium subscription')
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
            error = current_form.errors.values()[0]
    return render(request, 'super_premium/publication.html', context={'form':current_form, 'error':error})

@login_required
def PostRequirement(request):
    """view to save the requirement posted by the company"""
    error = None
    current_form = None
    if request.method == 'GET':
        current_form = PostRequirementForm()

    if request.method == 'POST':
        current_form = PostRequirementForm(request.POST)
        if current_form.is_valid():
            if PostRequirementUtil(current_form.cleaned_data, request.user):
                return HttpResponse('Requirement has been posted')
            else:
                return HttpResponse('server error')
        else:
            error = current_form.error.values()[0]
    return render(request, 'requirement/post_requirement.html', {'error':error, 'form':current_form})

def SearchCompany(request):
    """This is just for searching company"""
    context=[]
    if request.method == 'GET':
        return render(request, 'search_company.html', context=None)
    if request.method=='POST':
        search_text = request.POST['search_text']
        search_result = CompanyModel.objects.filter(company_name__contains=search_text)
        for result in search_result:
            company_url = ('/company/' + result.company_name.replace (" ", "-") +'/')
            context.append({'company_name':result.company_name, 'company_url':company_url})
        return render(request, 'search_company.html', context={'search_result':context})

def SearchCompanyAjax(request):
    """ view to render companies in the database on ajax request when user search for companies to form alliances """
    search_qs = CompanyModel.objects.filter(is_approved=True)
    results = []
    for r in search_qs:
        results.append(r.company_name)
    resp = simplejson.dumps(results)
    return HttpResponse(resp, content_type='application/json')

def Test(request):
    """This is just for testing dummy code. This is for testing purpose only"""
    if request.method == 'GET':
        return render(request, 'test.html', context=None)
        # search_text = request.POST['search_text']
    if request.method=='POST':
        search_result = CompanyModel.objects.filter(company_name__contains='cheese')
