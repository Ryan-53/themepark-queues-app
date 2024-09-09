"""
Name: firebase_access.py
Author: Ryan Gascoigne-Jones

Purpose: Contains additional functions used to interact with remote DB
"""

from django.conf import settings
import requests
from requests import Response
import logging

logging.getLogger().setLevel(logging.DEBUG)

def add_notif(ride_id: int, user_email: str) -> None:

  firebase_url: str = settings.FIREBASE_DB_URL
  ride_url: str = f"{firebase_url}/notifications/{ride_id}"
  fetch_url: str = f"{ride_url}/user_emails.json"
  update_url: str = f"{ride_url}.json"

  # Gets list of current emails already signed up for notifications
  cur_emails_response: Response = requests.get(fetch_url)

  # Checks if notification for ride_id exists already and if so
  # retrieves the emails subscribed to it.
  cur_emails: list[str]
  if cur_emails_response.status_code == 200 and cur_emails_response.json():
    cur_emails = cur_emails_response.json()
  else:
    cur_emails = []

  if user_email not in cur_emails:
    cur_emails.append(user_email)

  # TODO: Log DB access
  ride_notif: dict = {
    'ride_id': ride_id,
    'user_emails': cur_emails
  }

  # Adds new user_email to list of subscribed email addresses if the
  # ride notification has already been created by another user,
  # otherwise it creates the ride notification using ride_id as the key
  fdb_response: Response = requests.patch(update_url, json=ride_notif)

  logging.debug(f"FirebaseDB PUT Response = {fdb_response.status_code}")


def main() -> None:
  
  return None

if __name__ == '__main__':
  main()