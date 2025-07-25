from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def films(request):
    return render(request, 'pages/films.html')

def customers(request):
    return render(request, 'pages/customers.html')
