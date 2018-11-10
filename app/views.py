from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    return redirect('/login')


def login(request):
    return render(request, 'login.html')


def search(request):
    return render(request, 'search.html')


def results(request):
    return render(request, 'results.html')
