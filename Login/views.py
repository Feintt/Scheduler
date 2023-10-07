from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import LoginForm
from django.db import DatabaseError
import requests
from requests.utils import dict_from_cookiejar


def handle_user_creation_or_fetch(userid):
    """Handles fetching or creating a Django user."""
    try:
        user, created = User.objects.get_or_create(username=userid)
        if created:
            user.set_unusable_password()
            user.save()
        return user
    except DatabaseError:
        return None


def login_view(request):
    """The Login page."""

    # If the user is already logged in, redirect them to the dashboard
    if request.user.is_authenticated:
        return redirect('schedule')

    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            try:
                # Get the user's PeopleSoft ID and password
                userid = form.cleaned_data['email'].split('@')[0]
                pwd = form.cleaned_data['password']
            except KeyError:
                message = 'Invalid form submission!'
                return render(request, 'Login/login.html', {'form': form, 'message': message})
            except IndexError:
                message = 'Invalid form submission!'
                return render(request, 'Login/login.html', {'form': form, 'message': message})

            session = requests.Session()

            authentication_url = 'http://flow-api:8000/user/login/'
            payload = {
                'username': userid,
                'password': pwd
            }
            response = session.post(authentication_url, data=payload)

            if response.json()['success'] is True:
                user = handle_user_creation_or_fetch(userid)
                if user:
                    login(request, user)
                    request.session['token'] = response.json()['token']
                    request.session['api_cookies'] = dict_from_cookiejar(session.cookies)
                    return redirect('schedule')
                else:
                    message = "There was an issue processing your request. Please try again later."
            else:
                message = 'Login failed!'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': message
    }
    return render(request, 'Login/login.html', context)


def logout_view(request):
    """The Logout page."""

    if request.user.is_authenticated:
        cookie = request.session['api_cookies']
        token = request.session['token']
        logout_url = 'http://flow-api:8000/user/logout/'
        headers = {
            'Authorization': 'token ' + token
        }
        requests.post(logout_url, headers=headers, cookies=cookie)
        logout(request)

    return redirect('login')


def redirect_login(request):
    return redirect('/login/')
