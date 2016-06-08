from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username', 'type': 'text'}),
                               label="Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control',
                                                                                     'placeholder': 'Password',
                                                                                     'type': 'password'}),
                               label="Password")
    user = None

    def clean(self):
        if self._errors:
            return

        user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if user:
            if user.is_active:
                self.user = user
            else:
                self._errors['username'] = self.error_class(["Your account is inactive, try to recover it."])
        else:
            self._errors['username'] = self.error_class(
                ["The account does not exist, or username/password combination is incorrect."])
        return self.cleaned_data

    def login(self, request):
        try:
            User.objects.get(username=request.POST['username'])
        except:
            return False
        if self.is_valid():
            auth.login(request, self.user)
            request.session.set_expiry(0)
            return True
        return False
