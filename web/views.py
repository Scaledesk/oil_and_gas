from django.shortcuts import render, render_to_response


# Create your views here.
from django.template import RequestContext


def register(request):
    return render_to_response("registration.html",
                              {})