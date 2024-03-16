from rest_framework.serializers import ModelSerializer
from base.models import Room

#takes the model Room and serialize it and produce a json format of it
class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__' #give all fields you can also specify as a list