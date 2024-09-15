from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.db.models import QuerySet
from .forms import CreateUserForm, LoginUserForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Ride
from django.conf import settings
import json

# Utility functions
from .utils import get_queue_data, add_notif

def home(request: HttpRequest) -> HttpResponse:
  """Provides data for tables of rides seperated by ride category"""

  template = loader.get_template('home.html')

  ## DYNAMIC_TODO: Make this change when a different park is requested
  park_id: int = 1

  rides: tuple[QuerySet, QuerySet] = get_queue_data(park_id=park_id)

  land_names: list[str] = ["Family", "Thrills"]

  context: dict = {
    'title': 'Homepage',
    'rides_list': rides,
    'land_names': json.dumps(land_names)
  }

  return render(request, 'home.html', context)


def register(request: HttpRequest) -> HttpResponse:

  form: CreateUserForm = CreateUserForm()

  # If the form has been submitted
  if request.method == 'POST':

    form = CreateUserForm(request.POST)
    if form.is_valid():

      form.save()

      return redirect("/login")

  context: dict = {
    'form': form
  }

  return render(request, 'register.html', context)


def login(request: HttpRequest) -> HttpResponse:

  form: LoginUserForm = LoginUserForm()

  # If the form has been submitted
  if request.method == "POST":

    form = LoginUserForm(request, data=request.POST)
    if form.is_valid():

      # Email used as username
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = auth.authenticate(request, username=username, password=password)

      if user is not None:
        auth.login(request, user)
        return redirect("/")

  context = {
    'form': form
  }

  return render(request, 'login.html', context)


@login_required(login_url="login")
def account(request: HttpRequest) -> HttpResponse:


  return render(request, 'account.html')


# TODO: Last view unit test todo
@login_required(login_url="login")
def logout(request) -> HttpResponse:

  auth.logout(request)

  return redirect("/")


def ride_info(request: HttpRequest, ride_id: int) -> HttpResponse:
  """Provides info about a specific ride and enables user to subscribe to
  email notifications for reopening. Handles PUT requests to firebase DB to
  store email notification data."""

  ### IMPROVE_TODO: Get live data to the ride_info page instead of just
  ### taking last updated home page data. (maybe request data for
  ### individual ride directly from queue-times.com?)
  ride: Ride = get_object_or_404(Ride, id=ride_id)

  ## IMPROVE_TODO: Handle when user is already subscribed
  ## - Hold subscribed state somewhere to check.
  ## This is currently handled by not adding duplicate email addresses to
  ## remote DB.
  subscribed: bool = False

  if request.method == "POST":
    if request.user.is_authenticated:

      ## IMPROVE_TODO: This type hint issue should be addressed
      user_email: str = request.user.email # type: ignore

      # Loads remote database url from settings
      db_url: str = settings.FIREBASE_DB_URL

      # IMPROVE_TODO: Maybe return status code to display on website
      # (maybe just log this and return None)
      ## DYNAMIC_TODO: Make park_id change depending on park
      add_notif(park_id=1, ride_id=ride_id, ride_name=ride.name, user_email=user_email, db_url=db_url)

      subscribed = True

  context = {
    'ride': ride,
    'subscribed': subscribed,
  }

  return render(request, 'ride_info.html', context)


def about(request: HttpRequest) -> HttpResponse:

  return render(request, 'about.html')