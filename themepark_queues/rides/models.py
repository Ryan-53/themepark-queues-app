from django.db import models

class Ride(models.Model):

  id = models.IntegerField(primary_key = True)
  name = models.CharField(max_length = 255)
  type = models.CharField(max_length = 255)
  open_state = models.BooleanField()
  wait_time = models.PositiveSmallIntegerField()
  last_updated = models.DateTimeField()

  def __str__(self) -> str:
    return self.name
  
# class User(models.Model):

#   email = models.EmailField(max_length=100)
#   password = models.CharField(max_length=255)

#   def __str__(self) -> str:
#     return self.email

