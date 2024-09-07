from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register', views.register, name='register'),
  path('login', views.login, name='login'),
  path('account', views.account, name='account'),
  path('logout', views.logout, name='logout'),
  path('ride-info/<int:ride_id>', views.ride_info, name='ride-info'),
  path('about', views.about, name='about')
]