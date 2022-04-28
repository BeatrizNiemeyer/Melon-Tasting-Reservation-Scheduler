import os
import json
from datetime import datetime

import crud
from model import db, User, Appointment, connect_to_db
import server

os.system("dropdb mtr_data")
os.system("createdb mtr_data")

connect_to_db(server.app)
db.create_all()

with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    username = user['username']
    
    new_user = crud.create_user(username) 
    db.session.add(new_user)
    db.session.commit()

    user_id = crud.get_user_id_by_username(username)
    date_str = user['date_str']
    time_str = user['time_str']
    appointment = crud.create_appointment(user_id, date_str, time_str)
    db.session.add(appointment)
    db.session.commit()
