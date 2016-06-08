from django.contrib import messages
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters


from .forms import LoginForm


@sensitive_post_parameters()
def login(request):
    redirect_url = request.POST.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, 'You have successfully logged in.')
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect('/')
        else: form = LoginForm(request.POST, auto_id=True)
    else:
        form = LoginForm()

    response_dict = {'form': form, 'next': redirect_url}
    return render(request, 'auth/login.html', response_dict)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')