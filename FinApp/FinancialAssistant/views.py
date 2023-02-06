from django.shortcuts import render
from django.http import HttpResponse


# def test_view(request):
#     return HttpResponse('This is test view!')

def index(request):
    return HttpResponse('Hello!')
