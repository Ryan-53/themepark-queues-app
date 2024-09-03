from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import QuerySet
from .models import User
from .api_request import get_queue_data
from .forms import RegisterUserForm, LoginUserForm

def home(request) -> HttpResponse:

  template = loader.get_template('home.html')

  ## DYNAMIC_TODO: Make this change when a different park is requested
  park_id: int = 1

  rides: tuple[QuerySet, QuerySet] = get_queue_data(park_id=park_id)

  context = {
    'title': 'Homepage',
    'rides_family': rides[0],
    'rides_thrill': rides[1]
  }

  return render(request, 'home.html', context)


def register(request) -> HttpResponse:

  # If the form has been submitted
  if request.method == "POST":

    form = RegisterUserForm(request.POST)
    if form.is_valid():

      user = User(
        email = form.cleaned_data['email'],
        password = form.cleaned_data['password']
      )

      user.save()

      return redirect('/')
    
    ## TODO: Handle invalid sign up details

  form = RegisterUserForm()

  context = {
    'title': 'User registration',
    'form': form
  }

  return render(request, 'register.html', context)


def login(request) -> HttpResponse:

  # If the form has been submitted
  if request.method == "POST":

    form = LoginUserForm(request.POST)
    if form.is_valid():

      ### TODO: Log in validation (email and password)

      return redirect('/')

  form = LoginUserForm()

  context = {
    'title': 'User registration',
    'form': form
  }

  return render(request, 'login.html', context)