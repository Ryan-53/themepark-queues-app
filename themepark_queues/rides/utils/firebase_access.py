"""
Name: firebase_access.py
Author: Ryan Gascoigne-Jones

Purpose: Contains additional functions used to interact with remote DB
"""

from django.conf import settings
import requests
from requests import Response
import logging

from dotenv import load_dotenv
import os

logging.getLogger().setLevel(logging.DEBUG)

def add_notif(park_id: int,
              ride_id: int,
              ride_name: str,
              user_email: str,
              db_url: str) -> None:
  """Adds the notification request to the remote DB for the specific
  ride_id for the given user_email"""

  #firebase_url: str = settings.FIREBASE_DB_URL
  firebase_url: str = db_url

  ride_url: str = f"{firebase_url}/notifications/{park_id}/{ride_id}"
  fetch_url: str = f"{ride_url}/user_emails.json"
  update_url: str = f"{ride_url}.json"

  # Gets list of current emails already signed up for notifications
  cur_emails_response: Response = requests.get(fetch_url)

  # Checks if notification for ride_id exists already and if so
  # retrieves the emails subscribed to it.
  cur_emails: list[str] = []
  if cur_emails_response.status_code == 200 and cur_emails_response.json():
    cur_emails = cur_emails_response.json()

  if user_email not in cur_emails:
    cur_emails.append(user_email)

  ride_notif: dict = {
    'ride_id': ride_id,
    'ride_name': ride_name,
    'user_emails': cur_emails
  }

  # Adds new user_email to list of subscribed email addresses if the
  # ride notification has already been created by another user,
  # otherwise it creates the ride notification using ride_id as the key
  fdb_response: Response = requests.patch(update_url, json=ride_notif)

  logging.debug(f"FirebaseDB PUT Response = {fdb_response.status_code}")


def main() -> None:

  load_dotenv()
  firebase_url: str = os.getenv('FIREBASE_DB_URL', "")

  add_notif(park_id=328,
            ride_id=13905,
            ride_name="Dragon's Fury",
            user_email="rgj@hotmail.co.uk",
            db_url=firebase_url)
  
  return None

if __name__ == '__main__':
  main()