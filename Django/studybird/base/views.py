from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm
from django.db.models import Q#enable one to search for something in multiple tables
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
"""
rooms=[
    {"id":1,"name":"alpha"},
    {"id":2,"name":"desighn with me"}
]
"""

rooms=None
def Login_Page(request):
    if request.user.is_authenticated:
        return redirect('home')
    page='Login'
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
           user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not Exist')
            return render(request,'base/login_register.html')

        user=authenticate(request,username=username,password=password)   #Authentication of user when he puts in his credentials 
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect Password')

    context={'page':page}
    return render(request,'base/login_register.html',context)
def Register_page(request):
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)   
            return redirect('home')         
            '''
user = form.save(commit=False):
If the form data is valid, this line creates a new user object using the data submitted through the form. The form.save() method is typically used to save form data to the database. By default, form.save() will create and save a new object in the database. However, when commit=False is passed as an argument, Django creates the object in memory but does not save it to the database immediately.
            '''
        else:
            messages.error(request,"An error occured during registration")
    
    return render(request,'base/login_register.html',{'form':form})
def logout_page(request):
    logout(request)
    return redirect('home')
def home(request):
    if request.method=='POST':
        msg_id=request.GET.get('q')
        print("ndesaaaaa",msg_id)
        msg=Message.objects.get(id=msg_id)
        msg.delete()
        return redirect('home')
    q=request.GET.get('q')
    if q !=None:#q = request.GET.get('q', '')In summary, the purpose of q = "" is to handle the case where the q parameter is not provided in the request, ensuring that the variable q is always a string and can be used safely in subsequent operations, such as filtering database queries.
        pass
    else:
       q=""
    #we use double underscore to go up the parent 
    #we are searching in the Room table in multiple colllumns  for q,,through Room table we can search in to other tables like to the topic in the name collumn
    #In summary, if q is an empty string, the query will return all Room objects because the conditions will match any room with an empty string in the name, description, or topic__name fields.
    #Q(topic__name__icontains=q) looks for rooms where the associated topic's name contains the empty string. If q is empty, it essentially matches rooms where the topic's name contains any substring, as an empty string is present in every string.
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
        
    topics=Topic.objects.all()
    rooms_count=rooms.count()

    all_messages=Message.objects.filter(
    Q(room__name__icontains=q)|
    Q(room__topic__name__icontains=q)

    )#.order_by('-created') instead of using this to display from latest we specify in the models to return data from the new ones to old ones
    print(topics)
    context={'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'all_messages':all_messages}
    return render(request,'base/home.html',context)
    
def room(request,pk):
    room=Room.objects.get(id=pk)
    """room.participants.add(request.user)
    room.save
    adding a user to a specific room/associating a user to a room
    """
    room_messages=room.message_set.all().order_by('-created')#goes to model named ,message and gets all messgaes related to that room using modelname_set.all().'-created' arranges the messages in descending order using created
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
        user=request.user,
        room=room,
        body=request.POST.get('body')#getting something from the post request
        
        )
        """
        if you send a message then automatically you are made to be a participant/you are added to the participants
        """
        room.participants.add(request.user)
        message.save()
        return redirect('room',pk=room.id)
    for messages in room_messages:
        print(messages.created,"brian")

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)
@login_required(login_url='/Login')
def delete(request):
    if request.method=='POST':
        request.user

@login_required(login_url="/Login")#it will restrict the user from acesing the create room apge and the user will be redirecetd to login oagr if he wants to create room
def create_room(request):
    form=RoomForm()
    if request.method=="POST":
        #print(request.POST.get('name'))
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='/Login')#when user want to uodate a room he will be redirected to login page first using @login_required decorator
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('you are not allowed here')
    if request.method=="POST":
        #print(request.POST.get('name'))
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='/Login')#when user want to uodate a room he will be redirected to login page first using @login_required decoratorComparing room.host and request.
#user checks if the currently logged-in user (request.user) is the same as the user who is the host of the room (room.host)So, when you access room.host, you're actually accessing the User object that is related to the Room instance through the ForeignKey relationship.
#For example, if you have a Room instance called my_room, my_room.host would give you the User object that is associated with the host of that room.
#Therefore, while room.host itself is not an object, it holds a reference to an object (an instance of the User model in this case) representing the host of the room.. 
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed here')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    page='room'
    context={'obj':room,'page':page}
    return render(request,'base/delete_room.html',context)

@login_required(login_url="/login")
def DeleteMessage(request,pk,room_id):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here')
    context={'obj':message,'room_id':room_id}
    if request.method=='POST':
        message.delete()
        return redirect('room',pk=room_id)
    return render(request,'base/delete_room.html',context)
    
def user_profile(request,pk):
    user=User.objects.get(id=pk)
    topics=Topic.objects.all()#Getting all topics associated with the user
    rooms=user.room_set.all()#getting all rooms associated with user
    all_messages=user.message_set.all()#getting all messages associated with the user
    context={'user':user,'rooms':rooms ,'all_messages':all_messages,'topics':topics}
    return render(request,'base/profile.html',context)

def edit_profile(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile',pk=user.id)

    return render(request,'base/edit_profile.html',{'form':form})