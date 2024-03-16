#from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer 

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET/api',
        'GET/api/rooms',# Represents a GET request to fetch a list of rooms.
        'GET/api/rooms/:id'# Represents a GET request to fetch a specific room identified by :id.

    ]
    #return JsonResponse(routes,safe=False)
    return Response(routes)
@api_view(['GET'])
def getRoom(request,pk):
    room=Room.objects.get(id=pk)
    serializer=RoomSerializer(room,many=False)#many = True means we are serializing more than one object
    #many=false will return one object instead of the entire array
    #objects like rooms cannot be converted automtically
    return Response(serializer.data)

@api_view(['GET'])
def getRooms(request):
    room=Room.objects.all()
    serializer=RoomSerializer(room,many=True)#many = True means we are serializing more than one object
    #many=false will return one object instead of the entire array
    #objects like rooms cannot be converted automtically
    return Response(serializer.data)










"""
#safe=True (Default):

When safe=True, the JsonResponse class expects the data to be a dictionary, as dictionaries can be safely converted to JSON objects.
If you attempt to pass a non-dictionary object (such as a list, tuple, or custom object) while safe=True, Django will raise a TypeError because these objects cannot be directly serialized to JSON.
safe=False:

Setting safe=False tells Django that the data passed to JsonResponse might not be a dictionary and that it should be serialized directly to JSON, bypassing the usual dictionary conversion.
When safe=False, Django will attempt to serialize the data provided to JSON directly, regardless of its type. This can include lists, tuples, and other non-dictionary data structures.
This mode allows for more flexibility in the data types that can be passed to JsonResponse, but it's important to ensure that the data you provide is safe and can be properly serialized to JSON.
Here's an example demonstrating the use of saf
"""