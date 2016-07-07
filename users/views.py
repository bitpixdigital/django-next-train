from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from next_train.forms import UserCreateForm

def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('next_train:index'))

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form
        #form = UserCreationForm()
        form = UserCreateForm()
    else:
        # Process completed form.
        # form = UserCreationForm(data=request.POST)
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to the home page.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('next_train:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
