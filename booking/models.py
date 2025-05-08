from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.TextField()

    def __str__(self):
        return f"Room #{self.number} - {self.capacity}"

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]

class Booking(models.Model):
    pass