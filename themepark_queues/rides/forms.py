from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

class CreateUserForm(UserCreationForm):
  """Create a user form"""

  class Meta:
    model = User
    fields = ['email', 'password1', 'password2']
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


    self.label_suffix = ''

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset(
        '',
        Field('email'),
        Field('password1'),
        Field('password2')
      ),
      Submit('submit', 'Sign up', css_class='button white'),
    )

    self.fields['email'].label = "Email"
    self.fields['password1'].label = "Password"
    self.fields['password2'].label = "Re-enter password"

  def save(self, commit=True):
    """Overides parent save method to add in username as the email"""

    # Call parent save method but don't commit to DB yet
    user = super().save(commit=False)

    user.username = self.cleaned_data.get('email')

    if commit:
      user.save()
    
    return user

class LoginUserForm(AuthenticationForm):
  """Authenticate/Login a user form"""

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

    self.fields['username'].label = "Email"
    self.fields['password'].label = "Password"