from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render


def index(request):
    return render(request,"registration/base.html",{})
