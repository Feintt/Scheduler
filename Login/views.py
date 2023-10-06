from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import LoginForm
from .auth_login import authenticate_people_soft
from django.db import DatabaseError


# If the user goes to the root URL, redirect them to the Login page
def redirect_login(request):
    return redirect('/login/')


def handle_people_soft_authentication(userid, pwd):
    """Handles authentication against PeopleSoft."""
    try:
        return authenticate_people_soft(userid, pwd)
    except Exception as e:
        # You can log the error here for debugging.
        return False


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

            if handle_people_soft_authentication(userid, pwd):
                user = handle_user_creation_or_fetch(userid)
                if user:
                    login(request, user)
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
