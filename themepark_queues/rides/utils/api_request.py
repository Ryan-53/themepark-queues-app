"""
Name: api_request.py
Author: Ryan Gascoigne-Jones

Purpose: Contains additional functions used to retrieve queue data from
  an API
"""

from django.db.models import QuerySet
import requests
from ..models import Ride

def get_queue_data(park_id: int) -> tuple[list[QuerySet], list[str]]:
  """Retrieves all current ride data for the park of park_id passed and
  updates database with it so it can be displayed"""

  # Gets a list of all rides with attributes in dictionaries
  rides_req_lands: list[dict] = get_rides(park_id=park_id)

  # List of all ride categories
  ride_categories: list[str] = create_rides(park_id=park_id,
                                       rides_lands=rides_req_lands)
  
  # Compiles list of rides to show in tables
  rides: list[QuerySet] = compile_rides_list(ride_categories=ride_categories)
  
  return (rides, ride_categories)


def get_rides(park_id: int) -> list[dict]:
  """ Sends GET request to queue-times.com for the specified park """

  response = requests.get(f"https://queue-times.com/parks/{park_id}/"\
                          "queue_times.json")

  # Converts json response into a dictionary of all rides
  rides_req_dict: dict = response.json()

  # Gets value of lands key into a list
  rides_req_lands: list[dict] = rides_req_dict['lands']

  return rides_req_lands


def create_rides(park_id: int, rides_lands: list[dict]) -> list[str]:
  """Creates rides in park from json and saves in local DB and compiles a
  list of ride categories/lands"""
  
  # Creates an object for each ride in the local DB
  ride_category: list[str] = []
  for i in range(len(rides_lands)):
    # Adds category name to list
    ride_category.append(rides_lands[i]['name'])

    for cur_ride in (rides_lands[i])['rides']:

      ride = Ride(
        id = cur_ride['id'],
        name = cur_ride['name'],
        category = ride_category[i],
        open_state = cur_ride['is_open'],
        wait_time = cur_ride['wait_time'],
        last_updated = cur_ride['last_updated']
      )
      ride.save()

  return ride_category


def compile_rides_list(ride_categories: list[str]) -> list[QuerySet]:
  """Compiles list of rides to show on tables on homepage"""

  # Creates a queryset for each ride category
  rides: list[QuerySet] = []
  for category in ride_categories:
    rides.append(Ride.objects.filter(category = category).order_by('name'))

  return rides


def main() -> None:
  
  return None # pragma: no cover

if __name__ == '__main__':
  main()
  