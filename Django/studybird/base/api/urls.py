from django.urls import path
from . import views
# python -m pip install django-cors-headers
#its used to sepcify the origins that are allowed to acces our pagess through our api's check documentation od django an corsheaders
urlpatterns=[
    path('',views.getRoutes),
    path('room/<str:pk>/',views.getRoom),
    path('rooms/',views.getRooms),
]