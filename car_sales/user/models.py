from django.db import models
from django.contrib.auth.models import User

class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=127, blank=True)
    email = models.EmailField(blank=True, null=True)
    car_image = models.ImageField(null=True)
    query = models.TextField(max_length=511)