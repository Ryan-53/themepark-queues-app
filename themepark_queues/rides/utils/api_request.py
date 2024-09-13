"""
Name: api_request.py
Author: Ryan Gascoigne-Jones

Purpose: Contains additional functions used to retrieve queue data from
  an API
"""

from django.db.models import QuerySet
import requests
from ..models import Ride

def get_queue_data(park_id: int) -> tuple[QuerySet, QuerySet]:
  """Retrieves all current ride data for the park of park_id passed and
  updates database with it so it can be displayed"""

  api_url = f"https://queue-times.com/parks/{park_id}/queue_times.json"

  response = requests.get(api_url)

  # Converts json response into a dictionary of all rides
  rides_req_dict = response.json()

  # Gets value of lands key into a list
  rides_req_lands = rides_req_dict['lands']

  ## DYNAMIC_TODO: Adjust so it can be used dynamically for other parks.
  ## Already implemented in web scraper.
  # Sets ride type to family as the first list of rides are all of that
  # type.

  ## IMPROVE_TODO: This could be incorporated into following loop using
  ## enumerate for higher efficiency
  ride_types: list[str] = []
  for category in rides_req_lands:
    ride_types.append(category['name'])

  # Creates an object for each ride in the local DB
  for i in range(len(rides_req_lands)):

    for cur_ride in (rides_req_lands[i])['rides']:

      ride = Ride(
        id = cur_ride['id'],
        name = cur_ride['name'],
        type = ride_types[i],
        open_state = cur_ride['is_open'],
        wait_time = cur_ride['wait_time'],
        last_updated = cur_ride['last_updated']
      )

      ride.save()
  
  ## DYNAMIC_TODO: Change so it filters by any type not just for AT
  return (Ride.objects.filter(type = 'Family').order_by('name'),
    Ride.objects.filter(type = 'Thrills').order_by('name'))


def main() -> None:
  
  return None

if __name__ == '__main__':
  main()
  