"""
Name: test_firebase_access.py
Author: Ryan Gascoigne-Jones

Purpose: Tests firebase_access.py file for accessing and adding ride
  notifications to the remote DB
"""

from django.test import TestCase
from unittest.mock import patch, Mock
from ..utils.firebase_access import add_notif, add_to_email_list, \
  get_notif_db_url, get_park_url, get_ride_url
import logging

logging.getLogger().setLevel(logging.ERROR)


class AddNotifTest(TestCase):

  @patch('rides.utils.firebase_access.requests.patch')
  @patch('rides.utils.firebase_access.add_to_email_list')
  @patch('rides.utils.firebase_access.get_ride_url')
  def test_add_notif(self, mock_get_ride_url, mock_add_to_email_list,
                     mock_patch):
    """Tests adding/updating a ride notification to the remote DB"""

    mock_get_ride_url.return_value = 'mocked_ride_url'
    mock_add_to_email_list.return_value = ['test@example.com']
    mock_response = Mock()
    mock_response.status_code = 200
    mock_patch.return_value = mock_response

    add_notif(park_id=1, ride_id=101, ride_name='Test Ride',
              user_email='test@example.com')

    mock_get_ride_url.assert_called_once_with(park_id=1, ride_id=101)
    mock_add_to_email_list\
      .assert_called_once_with(ride_url='mocked_ride_url',
                               user_email='test@example.com')
    mock_patch.assert_called_once_with('mocked_ride_url.json', json={
        'ride_id': 101,
        'ride_name': 'Test Ride',
        'user_emails': ['test@example.com']
    })


class AddToEmailListTest(TestCase):

  @patch('rides.utils.firebase_access.requests.get')
  def test_add_to_email_list(self, mock_get):
    """Tests adding a new email to the existing email list"""

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = ['existing@example.com']
    mock_get.return_value = mock_response

    emails = add_to_email_list('mocked_ride_url', 'new@example.com')

    mock_get.assert_called_once_with('mocked_ride_url/user_emails.json')
    self.assertEqual(emails, ['existing@example.com', 'new@example.com'])


class GetUrlsFunctionsTest(TestCase):
  """Tests the 3 functions used to retrieve the url of the firebase"""

  @patch('rides.utils.firebase_access.settings')
  def test_get_notif_db_url(self, mock_settings):

    # Mocks settings getting the firebase url from an env variable
    mock_settings.FIREBASE_DB_URL = 'https://mocked-firebase-url'

    url = get_notif_db_url()
    self.assertEqual(url, 'https://mocked-firebase-url/notifications')

  @patch('rides.utils.firebase_access.get_notif_db_url')
  def test_get_park_url(self, mock_get_notif_db_url):

    # Mocks the previous functions result of the notifications section in
    # the firebase DB.
    mock_get_notif_db_url.return_value = 'https://mocked-firebase-url/notifica'\
      'tions'
    
    url = get_park_url(1)
    self.assertEqual(url, 'https://mocked-firebase-url/notifications/1')

  @patch('rides.utils.firebase_access.get_park_url')
  def test_get_ride_url(self, mock_get_park_url):

    # Mocks the previous functions result of the area for storing
    # notifications for a specific park.
    mock_get_park_url.return_value = 'https://mocked-firebase-url/notification'\
      's/1'
    
    url = get_ride_url(1, 101)
    self.assertEqual(url, 'https://mocked-firebase-url/notifications/1/101')