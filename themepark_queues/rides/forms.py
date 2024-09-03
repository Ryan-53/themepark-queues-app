from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

class RegisterUserForm(forms.Form):
  email = forms.EmailField(label='email',
                           widget=forms.EmailInput,
                           max_length=100)
  
  password = forms.CharField(label='password',
                             widget=forms.PasswordInput,
                             max_length=100)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


    self.label_suffix = ''

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset(
        '',
        Field('email'),
        Field('password')
      ),
      Submit('submit', 'Sign up', css_class='button white'),
    )

    self.fields['email'].label = "Email"
    self.fields['password'].label = "Password"

class LoginUserForm(forms.Form):
  email = forms.EmailField(label='email',
                           widget=forms.EmailInput,
                           max_length=100)
  
  password = forms.CharField(label='password',
                             widget=forms.PasswordInput,
                             max_length=100)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


    self.label_suffix = ''

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Fieldset(
        '',
        Field('email'),
        Field('password')
      ),
      Submit('submit', 'Log in', css_class='button white'),
    )

    self.fields['email'].label = "Email"
    self.fields['password'].label = "Password"