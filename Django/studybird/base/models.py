from django.db import models
#
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
#customizing the user model to use this innstead of the original model
class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.CharField(null=True)

    avator=models.ImageField(null=True,default='mash_brian.jpg')
    #it uses a third party called pillow
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

class Topic(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    """
    When you add blank=True to a field in Django models, it means that the field is allowed to be left blank when creating or updating an object. This attribute is only applicable to fields that are not required (null=False), such as CharField, TextField, ForeignKey, etc.
    """
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:#arranging in an oredr starting with the new ones then the old ones
        ordering =['-updated','-created']
    def __str__(self):
        return self.name
    
    #after adding a model u need to make migration using "python manage.py makemigrations"
    #then run "python manage.py migrate"here pythin will go to the latest migration and run it

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

       
    class Meta:#arranging in an order starting with the new ones then the old ones
        ordering =['-updated','-created']
        
    def __str__(self):
        return self.body[0:50]
