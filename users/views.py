from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Registers a new user."""
    if request.method != 'POST':
        # Shows a blank form with fields 'username' and 'password'.
        form = UserCreationForm()
    else:
        # POST data submitted; validates the form.
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticates and log in the new user.
            new_user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password1'])
            login(request, new_user)
            # Shows a success message.
            messages.success(
                request,
                'Your account has successfully created!')

            # Redirects to the main page.
            return redirect(reverse('learning_log:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
