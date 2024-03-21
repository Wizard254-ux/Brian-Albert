#views.py
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for,Flask
from .models import Arduino_data,User,Messages,Sensor_data,Average_Temp
from . import db,socketio
from sqlalchemy import desc
from flask_login import login_required,current_user
from flask_socketio import emit,SocketIO



views=Blueprint('views',__name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
 arduino_data=None
 try:
      
      print("ndesaaaaaaaa")
      arduino_data=Sensor_data.query.filter_by(user_relation=current_user.id).order_by(desc(Sensor_data.date)).first()
      print("bjvj ehrghekg ebjerb ehgekge",arduino_data.temp)
      #avg_data()
      if arduino_data is None:
          flash(f"No data Associated with the email",category='error')
 except Exception as e:
      print(e)
      flash(f"Failed to fetch data from Arduino database: {str(e)}",category='error')
 return render_template("home.html", user=current_user,arduino_data=arduino_data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@views.route('/receive_data', methods=['POST','GET'])
def receive_data():
     #arduino post url=http://localhost:5000/receive_data
     if request.method == 'POST': 
        #we access the body of the api request using request.get_json()
        arduinodata = request.get_json()#Assuming the arduino sends data in form of json ,,convert it into a dictionary format
        moisture=arduinodata['moisture']#extracting data and email from arduinodata
        humidity=arduinodata.get('humidity')
        temp=arduinodata.get('temperature')
        #email=arduinodata['email']
        print(temp,moisture,humidity)
       
        if temp :
            if moisture:
               #create a new entry in the arduino data associated with the user
               new_data=Sensor_data(temp=temp,humidity=humidity,moisture=moisture,user_relation=1)
               db.session.add(new_data)
               db.session.commit()
               arduinodata={'moisture':moisture,'humidity':humidity,'temp':temp}
               print("albert")
               #return render_template("home.html",user=current_user,arduino_data=arduinodata)
               #emiting an socket event to specific room if their was no room specified it will emit event to all clients 
               print(new_data.temp)
               data={
                   "temp":new_data.temp,
                   "moisture":new_data.moisture,
                   "humidity":new_data.humidity
               }
               socketio.emit('update_data', data)#if u want only people in message sot listen for the event you would specify /messages as the namespace
               print("ndesa")

               flash('Data appended to existing record', category='success')
            else:
               flash('No user associated with the email', category='error')
        else:
            flash('Invalid data format or missing fields',category='error')
     else:
         flash('method not allowed',category='error')
         return jsonify({'error': 'Invalid request'}), 400   
     return jsonify({'success':data})


@views.route('/Messages', methods=['GET'])
@login_required
def messages():
 if request.method=='GET':
    messages=Messages.query.order_by(desc(Messages.date)).all()
    return render_template("Messages.html",user=current_user,messages=messages)
 else:
     return jsonify({'error':'Invalid request'})

from datetime import datetime, timedelta
from pytz import timezone
# Define the time_ago filter
@views.app_template_filter('time_ago')
def time_ago(date,timezone_str='UTC'):
    # Set the timezone for date
    date = timezone(timezone_str).localize(date)
    # Get the current time in the specified timezone
    now = datetime.now(timezone(timezone_str))
    delta = now - date

    if delta < timedelta(seconds=60):
        return 'Just now'
    elif delta < timedelta(minutes=60):
        return f'{delta.seconds // 60} minutes ago'
    elif delta < timedelta(hours=24):
        return f'{delta.seconds // 3600} hours ago'
    else:
        return f'{delta.days} days ago'

@socketio.on('message')
def message(msg):
    
    print(msg)
    print('who are you')
    new_message=Messages(data=msg,user_relation=current_user.id)
    db.session.add(new_message)
    db.session.commit()
    print(new_message.date)
    date=time_ago(new_message.date)
    message={
        "username":current_user.first_name,
        "created":date,
        "body":new_message.data
    }
    socketio.emit("message",message)

#finding average of temperatures per day

from datetime import datetime,time,timedelta,date

@views.route('/fetchData',methods=['GET'])
def avg_data():
      my_list=[]
      start_date=datetime.now()-timedelta(days=30)
      end_date=datetime.now()
      data_list=Sensor_data.query.filter(
          Sensor_data.date.between(start_date,end_date),
          Sensor_data.user_relation==current_user.id
      ).all()
      for i in range(30):
        sum_temp = 0
        count = 0
        date = datetime.now() - timedelta(days=i)
        for data in data_list:
            if data.date.date() == date.date():
                sum_temp += data.temp
                count += 1
        if count > 0:
            avg_temp = sum_temp / count
            my_list.append({'date': date.date(), 'avg_temp': avg_temp})
        
      my_labels=[]
      my_values=[]
      for data in my_list:
            avg_temp_obj=Average_Temp(avg_temp=data['avg_temp'],avg_temp_date=data['date'],user_relation=current_user.id)
            print(avg_temp_obj.avg_temp_date)
            my_labels.append(str(avg_temp_obj.avg_temp_date))
            my_values.append(str(avg_temp_obj.avg_temp))
      my_list.reverse()
      my_labels.reverse()
      data2={
            "labels":
                my_labels
            ,
            "values":my_values
        }
      print(data2)
      return jsonify(data2)