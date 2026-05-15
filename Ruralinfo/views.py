from django.shortcuts import render


def home(request):
    return render(request, 'base/base_home.html')