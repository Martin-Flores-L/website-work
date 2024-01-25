from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def bodiweb(request):
    if request.user.is_authenticated:
        return render(request, 'bodiweb_request/bodiweb.html')
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')
