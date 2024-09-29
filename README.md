# Themepark Queues App

A Django web app for viewing the live queue times of rides at themeparks

Accessible here: [themeparkqueues.co.uk](http://themeparkqueues.co.uk)

## Technologies Used

* Python 3.9
* Django
* SQLite3
* Firebase NoSQL Realtime Database

## Hosting

* Hosted on AWS using an EC2 instance.

## Other supplementary applications

* Interacts with an Azure functions app handling email notifications.

## Features

* Users can view wait times for themepark rides.
* Users can subscribe for email notifications of rides reopening when they are closed (only available once logged in).

## Features in Development

* Machine Learning models will predict how ride times will change.
* Other themeparks will be added.
* Subscribing for notifications if a wait time goes below a certain point.
* A User will be able to favourite certain rides.

# Installation and Running

* Python3.9

1. Install python requirements
2. Run django app: python manage.py runserver

### Configuration

Requires environment variables for the following:
* A firebase realtime database url
* Encryption key
* DJANGO_ENV set to 'dev' to use development settings

### Usage

Will be updated soon...

## Author

Ryan-53