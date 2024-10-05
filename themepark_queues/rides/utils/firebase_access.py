"""
Name: firebase_access.py
Author: Ryan Gascoigne-Jones

Purpose: Contains additional functions used to interact with remote DB
"""

from django.conf import settings
import requests
from requests import Response
import logging
import firebase_admin
from firebase_admin import credentials, db # type: ignore

logging.getLogger().setLevel(logging.DEBUG)

def add_notif(park_id: int,
              ride_id: int,
              ride_name: str,
              user_email: str) -> None:
  """Adds the notification request to the remote DB for the specific
  ride_id for the given user_email"""

  ## Authenticating service account used to initialise connection with remote DB
  cred = credentials.Certificate(settings.FIREBASE_AUTH_KEY)
  firebase_admin.initialize_app(cred, {
    'databaseURL': settings.FIREBASE_DB_URL
  })

  ride_url: str = get_ride_url(park_id=park_id, ride_id=ride_id)
  update_url: str = f"{ride_url}"

  # Creates list of all emails subscribed
  cur_emails: list[str] = add_to_email_list(ride_url=ride_url,
                                            user_email=user_email)
  
  logging.debug(cur_emails)

  ride_notif: dict = {
    'ride_id': ride_id,
    'ride_name': ride_name,
    'user_emails': cur_emails
  }

  # Adds new user_email to list if already exists, otherwise create a new
  # ride notification using ride_id as the key.
  ref = db.reference(update_url)
  fdb_response: Response = ref.update(ride_notif)

  logging.debug(f"Notification created")


def add_to_email_list(ride_url: str, user_email: str) -> list[str]:
  """Adds new email address to list of current emails subscribed"""

  fetch_url: str = f"{ride_url}/user_emails"
  # Gets list of current emails already signed up for notifications
  ref = db.reference(fetch_url)
  cur_emails: list[str] = ref.get()

  # Checks if notification for ride_id exists already and if so
  # retrieves the emails subscribed to it.
  if cur_emails:
    if user_email not in cur_emails:
      cur_emails.append(user_email)
  else:
    cur_emails = [user_email]

  return cur_emails


def get_notif_db_url() -> str:
  """ Produces the location in the remote DB where all the ride
  notification data is stored from environment variable """

  # Loading firebase URL from settings (to change remote DB change env
  # variable)
  #firebase_url: str = settings.FIREBASE_DB_URL
  #notif_url: str = f"{firebase_url}notifications"

  notif_url: str = f"notifications"

  return notif_url


def get_park_url(park_id: int) -> str:
  """Produces the location in the remote DB where all the ride
  notification data for a specific ride"""

  park_url: str = f"{get_notif_db_url()}/{park_id}"

  return park_url


def get_ride_url(park_id: int, ride_id: int) -> str:
  """Generates the prefix url for a specific rides notification
  data"""

  ride_url: str = f"{get_park_url(park_id=park_id)}/{ride_id}"

  return ride_url


def main() -> None:

  return None

if __name__ == '__main__':
  main()