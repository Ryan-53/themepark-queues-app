from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

class CreateUserForm(UserCreationForm):
  """ Create a user form """

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


    self.label_suffix = ''

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset(
        '',
        Field('username'),
        Field('email'),
        Field('password1'),
        Field('password2')
      ),
      Submit('submit', 'Sign up', css_class='button white'),
    )

    self.fields['username'].label = "Username"
    self.fields['email'].label = "Email"
    self.fields['password1'].label = "Password"
    self.fields['password2'].label = "Re-enter password"

class LoginUserForm(AuthenticationForm):
  """ Authenticate/Login a user form """

  # TODO: Change username to email
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


    self.label_suffix = ''

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset(
        '',
        Field('username'),
        Field('password')
      ),
      Submit('submit', 'Log in', css_class='button white'),
    )

    self.fields['username'].label = "Username"
    self.fields['password'].label = "Password"