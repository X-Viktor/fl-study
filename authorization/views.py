from django.contrib.auth.views import LoginView
from django.views import generic

from .forms import SignUpForm, SignInForm


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(SignInView, self).get_context_data(**kwargs)
        context['title'] = 'Вход'
        context['button_title'] = 'Войти'
        return context


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['button_title'] = 'Зарегистрироваться'
        return context
