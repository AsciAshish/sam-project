from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class EmailPass(models.Model):
    email = models.CharField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.email

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    something = models.CharField(max_length=255, blank=True)
    option1 = models.IntegerField(blank=True)
    option2 = models.IntegerField(blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"Data for {self.user.username}"