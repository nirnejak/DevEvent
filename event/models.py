from django.db import models

#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Paradigm(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    paradigm = models.ForeignKey(Paradigm, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class User(AbstractUser):
    user_type = models.CharField(max_length=20)

class Programmer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    languages = models.ManyToManyField(Language)
    company = models.CharField(max_length=50)
    experience = models.IntegerField()

    def __str__(self):
        return self.user.username

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    location = models.CharField(max_length=50)


    def __str__(self):
        return self.user.username

class EventType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    venue = models.TextField()
    date = models.DateField(auto_now_add=True, blank=True)
    organizer = models.ForeignKey(Organizer, on_delete = models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, blank=True)
    programmers = models.ManyToManyField(Programmer, blank=True)
        
    def __str__(self):
        return self.name