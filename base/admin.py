from django.contrib import admin

# Register your models here.

from .models import Activitati,Topic,Message,Goal

admin.site.register(Activitati)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Goal)

