"""
Name: test_api_request.py
Author: Ryan Gascoigne-Jones

Purpose: Tests api_request.py file for requesting queue data from
  queue-times.com
"""

from django.test import TestCase
from ..models import Ride
from unittest.mock import patch, MagicMock
from ..utils.api_request import get_rides, create_rides, compile_rides_list


class GetRidesTest(TestCase):

  def setUp(self):
    """Sets up mock response data"""
  
    self.mock_response_data = {
      'lands': [
        {
          'name': 'Family Land',
          'rides': [
            {
              'id': 1,
              'name': 'Family Ride 1',
              'is_open': True,
              'wait_time': 30,
              'last_updated': '2023-09-12T12:00:00Z'
            }
          ]
        },
        {
          'name': 'Thrill Land',
          'rides': [
            {
              'id': 2,
              'name': 'Thrill Ride 1',
              'is_open': False,
              'wait_time': 0,
              'last_updated': '2023-09-12T12:05:00Z'
            }
          ]
        }
      ]
    }

  @patch('rides.utils.api_request.requests.get') # Mocks the GET request
  def test_get_rides(self, mock_get):
    """Tests the function gets the list of rides in the correct format
    and doesn't distort them from the data retrieved from the API"""

    # Mocks the response object returned by requests.get
    mock_response = MagicMock()
    mock_response.json.return_value = self.mock_response_data
    mock_get.return_value = mock_response

    # Calls the function
    result = get_rides(park_id=1)

    # Verifies the structure of the result
    expected_result = [
      {
        'name': 'Family Land',
        'rides': [
          {
            'id': 1,
            'name': 'Family Ride 1',
            'is_open': True,
            'wait_time': 30,
            'last_updated': '2023-09-12T12:00:00Z'
          }
        ]
      },
      {
        'name': 'Thrill Land',
        'rides': [
          {
            'id': 2,
            'name': 'Thrill Ride 1',
            'is_open': False,
            'wait_time': 0,
            'last_updated': '2023-09-12T12:05:00Z'
          }
        ]
      }
    ]

    # Checks the result is as expected
    self.assertEqual(result, expected_result)

    # Checks the correct URL was called
    mock_get.assert_called_once_with("https://queue-times.com/parks/1/queue_times.json")


class CreateRidesTest(TestCase):

  def setUp(self):
    """Sets up rides_lands list of lands and rides to test"""

    # Mock input data structure for rides_lands
    self.rides_lands = [
      {
        'name': 'Family',
        'rides': [
          {
            'id': 1,
            'name': 'Family Ride 1',
            'is_open': True,
            'wait_time': 30,
            'last_updated': '2023-09-12T12:00:00Z'
          },
          {
            'id': 2,
            'name': 'Family Ride 2',
            'is_open': False,
            'wait_time': 0,
            'last_updated': '2023-09-12T12:30:00Z'
          }
        ]
      },
      {
        'name': 'Thrills',
        'rides': [
          {
            'id': 3,
            'name': 'Thrill Ride 1',
            'is_open': True,
            'wait_time': 20,
            'last_updated': '2023-09-12T12:45:00Z'
          }
        ]
      }
    ]

  def test_create_rides_categories(self):
    """Tests that the ride categories are correctly found"""

    # Call the function with mocked data
    result = create_rides(park_id=1, rides_lands=self.rides_lands)

    # Assert that ride categories are returned correctly
    self.assertEqual(result, ['Family', 'Thrills'])

  @patch('rides.utils.api_request.Ride') # Mocks the Ride model
  def test_create_rides_rides_created(self, mock_ride):
    """Tests the creation of multiple ride objects in DB"""

    result = create_rides(park_id=1, rides_lands=self.rides_lands)

    # Assert that Ride objects were created and saved with the correct
    # values
    self.assertEqual(mock_ride.call_count, 3)  # 3 rides in total

    # Check that the save method was called for each ride
    self.assertEqual(mock_ride.return_value.save.call_count, 3)

  @patch('rides.utils.api_request.Ride')
  def test_create_rides_rides_correct(self, mock_ride):
    """Tests the correctness of created ride objects in DB"""

    result = create_rides(park_id=1, rides_lands=self.rides_lands)

    # Check the ride's attributes
    mock_ride.assert_any_call(
      id=1,
      name='Family Ride 1',
      category='Family',
      open_state=True,
      wait_time=30,
      last_updated='2023-09-12T12:00:00Z'
    )
    mock_ride.assert_any_call(
      id=2,
      name='Family Ride 2',
      category='Family',
      open_state=False,
      wait_time=0,
      last_updated='2023-09-12T12:30:00Z'
    )

  @patch('rides.utils.api_request.Ride')
  def test_create_rides_empty(self, mock_ride):
    """Tests the function passing in an empty list"""

    # Test with empty rides_lands list
    result = create_rides(park_id=1, rides_lands=[])

    # Assert that no categories are returned and no rides were created
    self.assertEqual(result, [])
    mock_ride.assert_not_called()


class CompileRidesListTest(TestCase):

  @patch('rides.models.Ride.objects.filter')  # Mocks the Ride model's filter method
  def test_compile_rides_list(self, mock_filter):
    """Tests compiling a populated list of rides"""
    
    # Mock the queryset that would be returned for each category
    mock_qs_family = MagicMock()  # Mock queryset for 'Family'
    mock_qs_thrill = MagicMock()  # Mock queryset for 'Thrills'

    # Mock the order_by call to return the same mock queryset
    mock_qs_family.order_by.return_value = mock_qs_family
    mock_qs_thrill.order_by.return_value = mock_qs_thrill

    # Defines what Ride.objects.filter should return (input category)
    mock_filter.side_effect = [
        mock_qs_family,
        mock_qs_thrill
    ]

    # Calls the function
    ride_categories = ['Family', 'Thrills']
    result = compile_rides_list(ride_categories)

    # Verify that the filter method was called with the correct arguments
    mock_filter.assert_any_call(category='Family')
    mock_filter.assert_any_call(category='Thrills')

    # Verify the function returns the expected result (list of querysets)
    self.assertEqual(result, [mock_qs_family, mock_qs_thrill])

  @patch('rides.models.Ride.objects.filter')
  def test_compile_rides_list_empty(self, mock_filter):
    """Tests compiling an empty list of rides"""

    # Mock an empty queryset return
    mock_filter.return_value = MagicMock()

    # Call the function with an empty ride category list
    result = compile_rides_list([])

    # Verify that no filter call was made
    mock_filter.assert_not_called()

    # Verify that the result is an empty list
    self.assertEqual(result, [])