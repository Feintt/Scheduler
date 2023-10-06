from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import LoginForm
from .auth_login import authenticate_people_soft


# If the user goes to the root URL, redirect them to the Login page
def redirect_login(request):
    return redirect('/login/')


def login_view(request):
    """
    The Login page.

    This is the page that the user will see when they go to the Login URL or the root URL.
    """

    # If the user is already logged in, redirect them to the dashboard
    if request.user.is_authenticated:
        return redirect('schedule')

    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['email'].split('@')[0]
            pwd = form.cleaned_data['password']
            if authenticate_people_soft(userid, pwd):
                # Create user if they don't exist, otherwise just login
                user, created = User.objects.get_or_create(username=userid)
                if created:
                    # If a new user was created, set an unusable password,
                    # This is because the authentication is managed by PeopleSoft, not Django's auth
                    user.set_unusable_password()
                    user.save()

                # Directly log the user into Django's session without re-authenticating
                login(request, user)
                # Redirect to a dashboard or home page after successful login
                return redirect('schedule')
            else:
                message = 'Login failed!'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': message
    }
    return render(request, 'Login/login.html', context)
