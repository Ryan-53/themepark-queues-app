"""
Name: test_views.py
Author: Ryan Gascoigne-Jones

Purpose: Tests models.py file
"""

from django.test import TestCase
from datetime import datetime
from ..models import Ride
from django.utils import timezone

# Create your tests here.
class RideModelTest(TestCase):
  """Tests the Ride model"""

  def setUp(self):
    """Sets up state of object before running tests"""

    self.ride = Ride.objects.create(
      id = 1,
      name = "Ride test placeholder",
      category = "Thrills",
      open_state = True,
      wait_time = 25,
      # timezone.now() is used instead of datetime.now() so it is a timezone
      # aware datetime object
      last_updated = timezone.now() 
    )

  def test_ride_creation(self):
    """Tests that a Ride object is created properly"""

    self.assertEqual(self.ride.name, "Ride test placeholder")
    self.assertEqual(self.ride.category, "Thrills")
    self.assertEqual(self.ride.open_state, True)
    self.assertEqual(self.ride.wait_time, 25)
    self.assertIsInstance(self.ride.last_updated, datetime)

  def test_string_representation(self):
    """Tests the string representation of the Ride object"""

    self.assertEqual(str(self.ride), "Ride test placeholder")

  def test_ride_id_field(self):
    """Tests the ride id field is correct and set as primary key"""

    self.assertEqual(self.ride.id, 1)
    self.assertTrue(Ride._meta.get_field('id').primary_key)

  def test_name_field_constraints(self):
    """Tests the name field for length constraints"""

    max_length = Ride._meta.get_field('name').max_length
    self.assertEqual(max_length, 255)

  def test_cat_field_constraints(self):
    """Tests the category field for length constraints"""

    max_length = Ride._meta.get_field('category').max_length
    self.assertEqual(max_length, 255)

  def test_wait_time_positive(self):
    """Tests that the wait_time is positive"""

    self.assertGreaterEqual(self.ride.wait_time, 0)

  def test_open_state_boolean_field(self):
    """Tests that open_state can only be True or False"""

    ride_closed = Ride.objects.create(
      id = 2,
      name = "Ride test placeholder 2",
      category = "Thrills",
      open_state = False,
      wait_time = 25,
      last_updated = timezone.now()
    )

    self.assertFalse(ride_closed.open_state)
    self.assertTrue(self.ride.open_state)