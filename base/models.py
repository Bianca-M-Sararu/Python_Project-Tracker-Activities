from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Activitati(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    date_time_done = models.DateTimeField(null=True, blank=True)
    rating_intensity = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])  # Add validators
    hours = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(23)])
    minutes = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    seconds = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    duration_in_seconds = models.IntegerField(default=0)
    #participant=
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ['-updated' , '-created'] #liniuta reprezinta cel mai nou el adaugat, fara - rep de la cel mai vechi la cel mai nou

    def __str__(self) :
        return self.name
    
    def save(self, *args, **kwargs):
        self.duration_in_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        super().save(*args, **kwargs)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activitati = models.ForeignKey(Activitati,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.body[0:50]

class Goal(models.Model):
    GOAL_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPES, default='daily')
    topics = models.ManyToManyField(Topic, blank=True)

    def __str__(self):
        return self.description

