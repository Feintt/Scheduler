from django.shortcuts import render, redirect
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
    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['email'].split('@')[0]
            pwd = form.cleaned_data['password']
            if authenticate_people_soft(userid, pwd):
                message = 'Login successful!'
            else:
                message = 'Login failed!'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': message
    }
    return render(request, 'Login/login.html', context)
