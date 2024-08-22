from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from .models import Ride

def home(request):

  template = loader.get_template('index.html')

  api_url = "https://queue-times.com/parks/1/queue_times.json"

  response = requests.get(api_url)

  # Converts json response into a dictionary of all rides
  rides_req_dict = response.json()

  # Gets value of lands key into a list
  rides_req_lands = rides_req_dict['lands']

  # Sets ride type to family as the first list of rides are all of that type
  ride_type = 'Family'
  for i in range(2):

    # Converts list of rides into a list of dicts of each ride separated by 
    # ride type
    ride_category = (rides_req_lands[i])['rides']

    # Number of rides in category
    num_rides_of_type = len(ride_category)

    for j in range(num_rides_of_type):

      # Gets dict of a single ride in list
      cur_ride = ride_category[j]

      ride = Ride(
        id = cur_ride['id'],
        name = cur_ride['name'],
        type = ride_type,
        open_state = cur_ride['is_open'],
        wait_time = cur_ride['wait_time'],
        last_updated = cur_ride['last_updated']
      )

      ride.save()

    ride_type = 'Thrill'

  # Retrieves lists of rides from ride table in DB (split into family and thrill lists)
  rides_family = Ride.objects.filter(type = 'Family').order_by('name')
  rides_thrill = Ride.objects.filter(type = 'Thrill').order_by('name')

  context = {
    'title': 'Homepage',
    'rides_family': rides_family,
    'rides_thrill': rides_thrill
  }

  return render(request, 'index.html', context)