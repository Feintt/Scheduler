from django.shortcuts import render, redirect
from django.http import HttpResponse


# If the user goes to the root URL, redirect them to the Login page
def redirect_login(request):
    return redirect('/login/')


def login(request):
    """
    The Login page.

    This is the page that the user will see when they go to the Login URL or the root URL.
    """
    return render(request, 'Login/login.html')
