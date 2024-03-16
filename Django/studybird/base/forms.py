from django.forms import ModelForm
from .models import Room,User


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__' #this specify that i want to render all fields here i can also use a list to specify the fields i want to render
        exclude=['host','participants'] #i'm excluding the room part so i wont see the room part

class UserForm(ModelForm):
  class Meta:
    model=User
    fields=['username','email']
