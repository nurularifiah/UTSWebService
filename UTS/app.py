# 6B - 19090045 - NURUL ARSIYATI 
# 6B - 19090085 - NURUL ARIFIAH GUNARSIH
# 6B - 19090101 - MOH. SYAEFUDIN FIKRI
# 6B - 19090113 - MULYANA PUTRIYANI 

from pickle import TRUE
from flask import Flask,request,jsonify
import random, os, string
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import check_password_hash
from sqlalchemy import DATETIME, TIMESTAMP

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "UtsWebService.db"))
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class logs(db.Model):
    created_at = db.Column(TIMESTAMP, default=datetime.datetime.now, unique=False,nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
class events(db.Model):
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
    event_creator = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=True)
    event_start_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_start_lat= db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_start_lng =db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_end_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
class users(db.Model):
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
    token = db.Column(db.String(20), unique=False,nullable=True, primary_key=False)
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
@app.route('/api/v1/users/create/', methods=['POST'])
def register():
    password = request.json['password']
    username = request.json['username']
    user = users(username=username,password=password,token= '')
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg" : "registrasi sukses"}), 200
@app.route('/api/v1/users/login/', methods=['POST'])
def login():
    password = request.json['password']
    username = request.json['username']
    user= users.query.filter_by(username=username).first()
    n=13
    if not user or not check_password_hash(user.password, password):
           tkn = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
           user.token= tkn
           db.session.commit()
    return jsonify({"msg": "login sukses","token": tkn,}), 200
@app.route('/api/v1/events/create/', methods=['POST'])
def event():
    token = request.json['token']
    username=users.query.filter_by(token=token).first()
    user = str(username.username)
    event_name = request.json['event_start_time']
    event_start_time = request.json['event_start_time']
    event_start_time_obj = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M')
    event_end_time = request.json['event_end_time']
    event_end_time_obj = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M')
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']
    eventt = events(event_creator = user,
                    event_name = event_name,
                    event_start_time = event_start_time_obj,
                    event_end_time = event_end_time_obj,
                    event_start_lat = event_start_lat,
                    event_start_lng = event_start_lng,
                    event_finish_lat = event_finish_lat,
                    event_finish_lng = event_finish_lng)
    db.session.add(eventt)
    db.session.commit()
    return jsonify({"msg": "membuat event sukses"}), 200

@app.route('/api/v1/logs', methods=['POST'])
def create_logs():
    token = request.json['token']
    username=users.query.filter_by(token=token).first()
    user=str(username.username)
    print(user)
    log = logs(username = format(user), event_name = request.json['event_name'],log_lat = request.json['log_lat'], log_lng = request.json['log_lng'])
    db.session.add(log)
    db.session.commit()
    return jsonify({"msg": "Log berhasil dibuat"}), 200

@app.route('/api/v1/users/logs/<token>/<event_name>', methods=['GET'])
def view_logs(token,event_name):
    view= logs.query.filter_by(event_name=event_name).all()
    
    log = []

    for i in view:
        dictlogs = {}
        dictlogs.update({"username": i.username,"log_lat": i.log_lat, "log_lng": i.log_lng, "create_at": i.created_at})
        log.append(dictlogs)
    return jsonify(log), 200

if __name__ == '__main__':
  app.run(debug = True, port=5000)
    