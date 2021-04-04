from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm, SignInForm


class SignInView(LoginView):
    form_class = SignInForm
    success_url = reverse_lazy('signin')
    template_name = 'registration/signin.html'


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signin')
    template_name = 'registration/signup.html'
