from django.contrib import admin
from .models import User,Message,SensorData
# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(SensorData)