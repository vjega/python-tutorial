from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return  HttpResponse("Hello Admin Page")

def logout(request):
    return HttpResponse("Logging Out of the system")

def forum(request):
    return HttpResponse("Forum module will be taken up later")
