from django.shortcuts import render, redirect
from .forms import LoginForm


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
            # Handle the login logic here
            pass
    else:
        form = LoginForm()

    context = {
        'form': form,
        'message': message
    }
    return render(request, 'Login/login.html', context)
