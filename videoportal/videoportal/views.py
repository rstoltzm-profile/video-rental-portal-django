from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This is Main Map viewer")

#this is about viewer
def about(request):
    return HttpResponse("This is About Page")

