"""
Name: test_views.py
Author: Ryan Gascoigne-Jones

Purpose: Tests views.py file for all interaction with user views and html
  files
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, get_user
from django.contrib import auth
from django.http import HttpRequest
from unittest.mock import patch
import json
from ..models import Ride
from django.utils import timezone
from django.conf import settings


class HomeViewTest(TestCase):

  def setUp(self):
    """Simulates get_queue_data function as a mock api request"""

    self.mocked_rides = (['family_ride_1', 'family_ride_2'], ['thrill_ride_1', 'thrill_ride_2'])
    self.land_names = ["Family", "Thrills"]

  @patch('rides.views.get_queue_data')
  def test_home_view_rendered(self, mock_get_queue_data):
    """Tests that the homepage is rendered correctly"""

    #
    mock_get_queue_data.return_value = self.mocked_rides
    response = self.client.get(reverse('home'))

    # Checks page is rendered properly
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')

  @patch('rides.views.get_queue_data')
  def test_home_view_context_rides(self, mock_get_queue_data):
    """Tests that ride context is passed correctly"""

    mock_get_queue_data.return_value = self.mocked_rides
    response = self.client.get(reverse('home'))

    # Check rides list is in context
    self.assertIn('rides_list', response.context)
    # Check context contains rides
    self.assertEqual(response.context['rides_list'], (['family_ride_1', 'family_ride_2'], ['thrill_ride_1', 'thrill_ride_2']))

  @patch('rides.views.get_queue_data')
  def test_home_view_context_lands(self, mock_get_queue_data):
    """Tests that ride category/land context is passed correctly"""

    mock_get_queue_data.return_value = self.mocked_rides
    response = self.client.get(reverse('home'))

    # Check context contains land_names and it's correctly converted to JSON
    self.assertIn('land_names', response.context)
    self.assertEqual(response.context['land_names'], json.dumps(self.land_names))

  @patch('rides.views.get_queue_data')
  def test_home_view_contains_table_headers(self, mock_get_queue_data):
    """Tests that headers of tables are correct"""

    mock_get_queue_data.return_value = self.mocked_rides
    response = self.client.get(reverse('home'))

    # Tests table headers
    self.assertContains(response, 'Family')
    self.assertContains(response, 'Thrills')

  @patch('rides.views.get_queue_data')
  def test_home_view_displays_rides(self, mock_get_queue_data):
    """Tests that homepage contains the correct data in ride tables"""

    # Mock return value for get_queue_data
    mocked_rides = [
      {'name': 'family_ride_1', 'wait_time': 30, 'open_state': True},
      {'name': 'family_ride_2', 'wait_time': 20, 'open_state': True},
      {'name': 'thrill_ride_1', 'wait_time': 10, 'open_state': True},
      {'name': 'thrill_ride_2', 'wait_time': 5, 'open_state': True},
    ]

    mock_get_queue_data.return_value = ([ride for ride in mocked_rides[:2]], [ride for ride in mocked_rides[2:]])
    response = self.client.get(reverse('home'))

    # Check that the page contains the ride names and wait times
    self.assertContains(response, 'family_ride_1')
    self.assertContains(response, '30')
    self.assertContains(response, 'family_ride_2')
    self.assertContains(response, '20')
    self.assertContains(response, 'thrill_ride_1')
    self.assertContains(response, '10')
    self.assertContains(response, 'thrill_ride_2')
    self.assertContains(response, '5')


class RegisterViewTest(TestCase):

  def setUp(self):
    """Sets up valid registration data to be tested"""

    self.valid_data = {
      'email': 'testuser@example.com',
      'password1':'testpassword',
      'password2':'testpassword'
    }

  def test_register_view_get(self):
    """Tests register form is displayed on GET requests"""

    response = self.client.get(reverse('register'))

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'register.html')
    # Ensures form is passed in context
    self.assertIn('form', response.context)
  
  def test_register_view_post_valid_data(self):
    """Tests that a user is created and user redirected upon valid
    form submission"""

    # POST valid_data through form
    response = self.client.post(reverse('register'), self.valid_data)

    # Check it redirects to homepage
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/login')

    # Check the user has been created in the DB
    self.assertTrue(User.objects.filter(email='testuser@example.com'))
  
  def test_register_view_post_invalid_data_email(self):
    """Tests that a user is not created and redirected with invalid
    data --> Page should be re-rendered"""

    invalid_data = {
      'email': 'wronguser',
      'password1':'testpassword',
      'password2':'testpassword'
    }

    response = self.client.post(reverse('register'), invalid_data)
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'form', 'email', "Enter a valid email address.")
  
  def test_register_view_post_invalid_data_password(self):
    """Tests that a user is not created and redirected with invalid
    data --> Page should be re-rendered"""

    invalid_data = {
      'email': 'wronguser@example.com',
      'password1':'testpassword',
      'password2':'differentpassword'
    }

    response = self.client.post(reverse('register'), invalid_data)
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")


class LoginViewTest(TestCase):

  def setUp(self):
    """Creates a user for login testing"""

    self.user = get_user_model().objects.create_user(
      username='testuser@example.com',
      email='testuser@example.com',
      password='testpassword'
      )

  def test_login_view_get(self):
    """Tests login form is displayed on GET requests"""

    response = self.client.get(reverse('login'))

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'login.html')
    # Ensures form is passed in context
    self.assertIn('form', response.context)

  def test_login_view_post_invalid_form(self):
    """Tests that invalid data doesn't authenticate user"""

    response = self.client.post(reverse('login'), {
      'username': '',
      'password': ''
    })

    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context['form'].is_valid())
  
  def test_login_view_post_valid_credentials(self):
    """Tests that valid data authenticates user and redirects to
    homepage"""

    response = self.client.post(reverse('login'), {
      'username': 'testuser@example.com',
      'password': 'testpassword'
    })

    # Check it redirects to homepage
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/') 

    # Check if the user is authenticated
    user = auth.get_user(self.client)
    self.assertTrue(user.is_authenticated)

  def test_login_view_post_invalid_credentials(self):
    """Tests that invalid credentials don't authenticate the user"""

    response = self.client.post(reverse('login'), {
      'username': 'wronguser@example.com',
      'password': 'wrongpassword'
    })

    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context['form'].is_valid())
    # Ensures form is passed in context
    self.assertIn('form', response.context)

    # Check if the user is authenticated
    user = auth.get_user(self.client)
    self.assertFalse(user.is_authenticated)


class AccountViewTest(TestCase):

  def setUp(self):
    """Sets up test user to log in to"""

    self.user = User.objects.create_user(
      username='testuser@example.com', 
      email='testuser@example.com', 
      password='testpass'
    )

  def test_account_view_authenticated(self):
    """Tests account view loads as expected if user is logged in"""

    self.client.login(username='testuser@example.com', password='testpass')
    response = self.client.get(reverse('account'))
    self.assertEqual(response.status_code, 200)

  def test_account_view_anonymous(self):
    """Tests account view redirects to login page if user is
    unauthenticated"""

    response = self.client.get(reverse('account'))
    self.assertRedirects(response=response,
                         expected_url='/login?next=/account',
                         status_code=302,
                         target_status_code=200,
                         fetch_redirect_response=True)


class LogoutViewTest(TestCase):

  def setUp(self):
    """Sets up test user to log in to"""

    self.user = User.objects.create_user(
      username='testuser@example.com', 
      email='testuser@example.com', 
      password='testpass'
    )

  def test_logout_redirects_anonymous(self):
    """Tests that an unauthenticated user should be redirected to the
    login page if trying to logout"""

    response = self.client.get(reverse('logout'))
    self.assertRedirects(response, '/login?next=/logout', 302, 200)

  def test_logout_authenticated_user(self):
    """Tests that an authenticated user can logout sucessfully and get
    redirected to the homepage"""

    # Log the user in
    self.client.login(username='testuser@example.com', password='testpass')

    # Ensure user is authenticated before logout
    user = get_user(self.client)
    self.assertTrue(user.is_authenticated)

    # Ensure the user is logged out and redirected to the homepage
    response = self.client.get(reverse('logout'))
    self.assertRedirects(response, '/')

    # Ensure user is no longer authenticated after logout
    user = get_user(self.client)
    self.assertFalse(user.is_authenticated)


class RideInfoViewTest(TestCase):

  def setUp(self):
    """Sets up test user to allow subscription and sets up Ride to see
    info"""

    self.user = User.objects.create_user(
      username='testuser@example.com', 
      email='testuser@example.com', 
      password='testpass'
    )

    # Create a Ride object
    self.ride = Ride.objects.create(
      id=1,
      name="Test Ride",
      category="Thrill",
      open_state=False,
      wait_time=30,
      last_updated=timezone.now()
    )
    
  # Mocks the add_notif function
  @patch('rides.views.add_notif')
  def test_ride_info_view_authenticated_user(self, mock_add_notif):
    """Tests that a user can subscribe if they are logged in"""

    # Logs user in
    self.client.login(username='testuser@example.com', password='testpass')

    # Post request simulates user subscribing
    response = self.client.post(reverse('ride-info', kwargs={'ride_id': self.ride.id}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['ride'], self.ride)
    self.assertTrue(response.context['subscribed'])

    # Check that add_notif was called once with correct arguments
    mock_add_notif.assert_called_once_with(
      park_id=1,
      ride_id=self.ride.id,
      ride_name=self.ride.name,
      user_email='testuser@example.com',
      db_url=settings.FIREBASE_DB_URL
    )

  def test_ride_info_view_anonymous_user(self):
    """Tests that a user cannot subscribe if they aren't logged in"""

    response = self.client.get(reverse('ride-info', kwargs={'ride_id': self.ride.id}))
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.context['subscribed'])


class AboutViewTest(TestCase):

  def test_about_view_rendered(self):

    response = self.client.get(reverse('about'))
    self.assertEqual(response.status_code, 200)

