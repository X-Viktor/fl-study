from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SignInForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'password']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'password')
