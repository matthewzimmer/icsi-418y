from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/search')


def login(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required
def search(request):
    return render(request, 'search.html')


@login_required
def results(request):
    return render(request, 'results.html')
