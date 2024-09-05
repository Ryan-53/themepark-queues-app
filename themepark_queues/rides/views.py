from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import QuerySet
from .api_request import get_queue_data
from .forms import CreateUserForm, LoginUserForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def home(request) -> HttpResponse:

  template = loader.get_template('home.html')

  ## DYNAMIC_TODO: Make this change when a different park is requested
  park_id: int = 1

  rides: tuple[QuerySet, QuerySet] = get_queue_data(park_id=park_id)

  land_names: list[str] = ['Family', 'Thrills']

  context: dict = {
    'title': 'Homepage',
    'rides_family': rides[0],
    'rides_thrill': rides[1],
    'rides_list': rides,
    'land_names': land_names
  }

  return render(request, 'home.html', context)


def register(request) -> HttpResponse:

  form = CreateUserForm()

  # If the form has been submitted
  if request.method == 'POST':

    form = CreateUserForm(request.POST)
    if form.is_valid():

      form.save()

      return redirect("/")

  context: dict = {
    'title': 'User registration',
    'form': form
  }

  return render(request, 'register.html', context)


def login(request) -> HttpResponse:

  form = LoginUserForm()

  # If the form has been submitted
  if request.method == "POST":

    form = LoginUserForm(request, data=request.POST)
    if form.is_valid():

      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not None:
        auth.login(request, user)
        return redirect("/")

  context = {
    'title': 'User registration',
    'form': form
  }

  return render(request, 'login.html', context)


@login_required(login_url="login")
def account(request) -> HttpResponse:


  return render(request, 'account.html')


def logout(request) -> HttpResponse:

  auth.logout(request)

  return redirect("/")