from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            # Log in the user and redirects him to main page.
            user = authenticate(
                request,
                username=request.POST['username'], 
                password=request.POST['password1'],
            )
            login(request, user)
            return HttpResponseRedirect(reverse('learning_log:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)

