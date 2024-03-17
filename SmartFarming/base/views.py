from django.shortcuts import render,redirect
from .models import User,Message
from .forms import RegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.serializers import serialize
from django.core import serializers

# Create your views here.
@login_required(login_url='/Login')
def home(request):
    return render(request,'base/home.html')

def Login_page(request):
 Page="Login"
 if request.method=='POST':
    email=request.POST.get('email')
    password=request.POST.get('password')
    print("albert")
    try:
        user=User.objects.get(email=email)
        print(user)
    except:
        messages.error(request,"user with email doesn't exist")
        return render(request,'base/login_page.html',{'page':Page})
    user=authenticate(email=email,password=password)
    if user is not None:
       login(request,user)
       return redirect('home')
    else:
       messages.error(request,"Incorrect Password! ")

 return render(request,'base/login_page.html',{'page':Page})

def register_page(request):
    
    if request.method=='POST':
       form=RegistrationForm(request.POST)
       print(request.POST)
       if form .is_valid():
          user=form.save(commit=False)
          user.username=user.username.lower()
          user.save()
          login(request,user)
          return redirect('home')
       else:
          print(form.errors)
          for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            # You can also pass the form instance with errors back to the template
    return render(request,'base/Login_page.html')
@login_required(login_url='/Login')
def chatts(request):
   if request.method=="POST":
     try:
      message=Message.objects.create(host=request.user,body=request.POST.get('text'))
     except Exception as e:
        print(e)
   all_msg=Message.objects.all()
   for i in all_msg:
      print(i.host.username,'hhvhvvvjv')
 
   return render(request,'base/chatts.html',{'all_msg':all_msg,})

def Logout_user(request):
   logout(request)
   return redirect('home')
def Farm_data(request):
   return render(request,'base/Farm_data.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData
@csrf_exempt
def data_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data['temperature']
            humidity = data['humidity']
            moisture = data['moisture']
            email=data['email']
            
            print(temperature)
            user=User.objects.get(email=request.user.email)
            # Save data to the database
            SensorData.objects.create(host=user,temp=temperature, humid=humidity, moisture=moisture)
            return JsonResponse({'message': 'Data received successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        #return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
        return render(request,'base/data_analysis')
    
def fetchData(request):
   print("mmmmmmmmmmmmmmmalbert")
   if request.method=='GET':
      print("brian albert")
      data=Message.objects.all()
      data_msg=[]
      for message in data:
        message_data={
           'body':message.body,
           'username':message.host.username,
           'created':message.created,
        }
        data_msg.append(message_data)
      return JsonResponse({'data':data_msg},safe=False)
      #return JsonResponse({"data":list(data.values())},safe=False)
   return JsonResponse({'error':'invalid request'})

    