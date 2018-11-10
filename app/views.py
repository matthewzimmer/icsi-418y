from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    return redirect('/login')


def login(request):
    return HttpResponse("TODO: Implement LOGIN UI.")


def search(request):
    return HttpResponse("TODO: Implement SEARCH UI.")


def results(request):
    return HttpResponse("TODO: Implement SEARCH RESULTS UI.")
