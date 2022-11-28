from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=32)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "username: %s"%(self.username)
