from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import LoginForm
from django.db import DatabaseError
import requests


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
            # Get the user's PeopleSoft ID and password
            userid = form.cleaned_data['email'].split('@')[0]
            pwd = form.cleaned_data['password']

            # Send post-request to http://flow_api:8000/user/login
            # If the user is authenticated, log them in

            response = requests.post(
                'http://flow-api:8000/user/login/',
                data={'username': userid, 'password': pwd}
            )

            if response.status_code == 200:
                user = handle_user_creation_or_fetch(userid)
                if user:
                    login(request, user)
                    request.session['token'] = response.json()['token']
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
        logout(request)

    return redirect('login')


def redirect_login(request):
    return redirect('/login/')
