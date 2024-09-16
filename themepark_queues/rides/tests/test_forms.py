"""
Name: test_forms.py
Author: Ryan Gascoigne-Jones

Purpose: Tests forms.py file's user login and registration form's
  back-end functionality
"""

from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import CreateUserForm, LoginUserForm

class CreateUserFormTests(TestCase):

  def test_create_user_form_valid_data(self):
    """Tests if the CreateUserForm is valid with proper data."""
    
    form_data = {
      'email': 'test@example.com',
      'password1': 'strongpassword123',
      'password2': 'strongpassword123'
    }
    form = CreateUserForm(data=form_data)
    self.assertTrue(form.is_valid())

  def test_create_user_form_invalid_email(self):
    """Tests if the CreateUserForm is invalid with incorrect email."""

    form_data = {
      'email': 'invalid-email',
      'password1': 'strongpassword123',
      'password2': 'strongpassword123'
    }
    form = CreateUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('email', form.errors)

  def test_create_user_form_password_mismatch(self):
    """Tests if the form catches mismatching passwords."""
    
    form_data = {
      'email': 'test@example.com',
      'password1': 'password123',
      'password2': 'password456'
    }
    form = CreateUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('password2', form.errors)

  def test_create_user_form_save(self):
    """Tests if the form correctly assigns email to username and saves."""
    
    form_data = {
      'email': 'test@example.com',
      'password1': 'strongpassword123',
      'password2': 'strongpassword123'
    }
    form = CreateUserForm(data=form_data)
    
    # Ensure form is valid before calling save
    self.assertTrue(form.is_valid())

    # Save form and check that the username is set to the email
    user = form.save(commit=False)
    self.assertEqual(user.username, 'test@example.com')

    # Now save to the database
    user.save()
    self.assertEqual(User.objects.count(), 1)
    self.assertEqual(User.objects.get().username, 'test@example.com')

class LoginUserFormTests(TestCase):

  def setUp(self):
    # Create a test user
    self.user = User.objects.create_user(
      username='test@example.com',
      email='test@example.com',
      password='strongpassword123'
    )
    self.user.save()

  def test_login_user_form_valid_data(self):
    """Tests if the LoginUserForm is valid with proper data."""

    form_data = {
      'username': 'test@example.com',
      'password': 'strongpassword123'
    }
    form = LoginUserForm(data=form_data)
    self.assertTrue(form.is_valid())

  def test_login_user_form_missing_password(self):
    """Tests if the form catches missing password."""

    form_data = {
      'username': 'test@example.com',
      'password': ''
    }
    form = LoginUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('password', form.errors)

  def test_login_user_form_missing_username(self):
    """Tests if the form catches missing username."""

    form_data = {
      'username': '',
      'password': 'password123'
    }
    form = LoginUserForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('username', form.errors)

