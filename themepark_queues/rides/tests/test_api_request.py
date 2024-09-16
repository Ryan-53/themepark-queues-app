"""
Name: test_api_request.py
Author: Ryan Gascoigne-Jones

Purpose: Tests api_request.py file for requesting queue data from
  queue-times.com
"""

from django.test import TestCase
from ..models import Ride
from unittest.mock import patch, MagicMock
from ..utils.api_request import get_queue_data, get_rides, create_rides, \
  compile_rides_list

class CompileRidesListTest(TestCase):

  # TODO: This fails + also work out what MagicMock does
  @patch('rides.models.Ride.objects.filter')  # Mock the Ride model's filter method
  def test_compile_rides_list(self, mock_filter):
    """Tests compiling a populated list of rides"""
    
    # Mock the queryset that would be returned for each category
    mock_qs_family = MagicMock()  # Mock queryset for 'Family'
    mock_qs_thrill = MagicMock()  # Mock queryset for 'Thrills'

    # Mock the order_by call to return the same mock queryset
    mock_qs_family.order_by.return_value = mock_qs_family
    mock_qs_thrill.order_by.return_value = mock_qs_thrill

    # Define what Ride.objects.filter should return based on input category
    mock_filter.side_effect = [
        mock_qs_family,  # First call to filter returns mock_qs_family
        mock_qs_thrill   # Second call to filter returns mock_qs_thrill
    ]

    # Define the categories to pass to compile_rides_list
    ride_categories = ['Family', 'Thrills']

    # Call the function being tested
    result = compile_rides_list(ride_categories)

    # Verify that the filter method was called with the correct arguments
    mock_filter.assert_any_call(category='Family')
    mock_filter.assert_any_call(category='Thrills')

    # Verify the function returns the expected result (a list of querysets)
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