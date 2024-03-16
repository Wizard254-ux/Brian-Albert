from django.urls import path
from . import views

urlpatterns=[
    path('edit-profile',views.edit_profile,name='edit-profile'),
    path('user-profile/<str:pk>',views.user_profile,name='user-profile'),
    path('Delete/',views.delete,name='delete'),
    path('delete-message/<str:pk>/<str:room_id>/',views.DeleteMessage,name="delete-message"),
    path('Login/',views.Login_Page,name='Login'),
    path('Register/',views.Register_page,name='Register'),
    path('Logout/',views.logout_page,name='Logout'),
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.create_room,name='createroom'),
    path('update_room/<str:pk>/',views.updateroom,name='updateroom'),
    path('deleteroom/<str:pk>/',views.deleteroom,name='deleteroom')
]