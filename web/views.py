from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic import View

from core.utils import registerCompany
from web.forms import CompanyRegistrationForm


class CompanyView(View):
    def get(self, request):
        """function to render the registration page"""
        return render(request, "registration.html", {'form': CompanyRegistrationForm()})

    def post(self, request):
        """function to handle the post request from the registration page"""
        # company_name = request.POST.get("company_name")
        # # user_name that will be split into first name and the lastname
        # username = request.POST.get("username")
        # company_email = request.POST.get("company_email")
        # ad_reference = request.POST.get("ad_reference")
        # password = request.POST.get("password")
        # user_id = request.POST.get("user_id", None)
        # is_created, response_text = registerCompany(company_name=company_name, company_email=company_email,
        #                                             password=password, ad_reference=ad_reference, user_id=None,
        #                                             username=username)
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            is_created, response_text = registerCompany(company_name=form.cleaned_data['company_name'],
                                                        company_email=form.cleaned_data['company_email'],
                                                        password=form.cleaned_data['password'],
                                                        ad_reference=form.cleaned_data['ad_reference'], user_id=None,
                                                        username=form.cleaned_data['username'])
            return HttpResponse(response_text)
        else:
            return render(request, "registration.html", {'form': CompanyRegistrationForm(),'errors':form.errors['__all__']})
