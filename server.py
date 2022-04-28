from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from datetime import datetime
from model import User, Appointment, connect_to_db
import os

app = Flask(__name__)
app.secret_key = "key"
app.jinja_env.undefined = StrictUndefined


times = ["00:30", "01:00", "01:30" ,"02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00",
"06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", 
"13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", 
"19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "00:00" ]

@app.route("/")
def login_page():
    """Show homepage"""

    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    """ Login with username"""

    #Getting data from the form
    username = request.form.get('username')

    user = crud.get_user_by_username(username)

    if user:
        session['user'] = crud.get_user_id_by_username(username)
        return redirect("homepage")
    else:
        flash('Information is incorrect, try again!')

    return redirect('/')


@app.route('/homepage')
def show_homepage():

    return render_template("homepage.html")


@app.route('/schedule_appointment', methods =['POST'])
def schedule_appointment():
    """Route to handle appointments"""

    if "user" in session:
        user_id = session["user"]

    date = request.form.get('date') 
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    print("#################")
    print(date)
    print(start_time)
    print(end_time)
    print(type(start_time))

  
    list_of_times = []
    for time in times:
        if (int(start_time[:2] + start_time[3:])) <= (int(time[:2] + time[3:])) and (int(end_time[:2] + end_time[3:])) >= (int(time[:2] + time[3:])):
           list_of_times.append(time)

    appointments_available = [] 
    all_appointments = crud.get_all_appointments_by_date(date)
    print(list_of_times)

    list_of_unavailable_times =[]
    for apt in all_appointments:
        if apt.user_id == user_id:
            flash("sorry, you already have an appointment that day!")
            return redirect('/homepage')

    for apt in all_appointments:
        list_of_unavailable_times.append(apt.time_str)



    for time in list_of_times:
        if time not in list_of_unavailable_times and time not in appointments_available:
            appointments_available.append(time)

    session['appointments_available'] = appointments_available
    final_appointments = []
    for apt in appointments_available:
        if int(apt[:2]) < 12:
            time = apt + "AM"
        elif int(apt[:2]) == 12:
            time = apt + "PM"
        else:
            time = str(int(apt[:2]) - 12) + apt[2:] + "PM"
        final_appointments.append(time)
        

    print(final_appointments)
        
    #get all the the objects, filtered by the selected date

    #for apt in appointments, if apt.user_id != user_id:
        # for time in list_of_times, if time != apt.time, apt append to list_avaible_times


    correct_date = date.split("-")
    year = correct_date[0] 
    month = correct_date[1]
    day = correct_date[2]

    if int(month) < 10:
        month = month[1:2]

    if int(day) < 10:
        day = day[1:2]

    final_date = month + "/" + day + "/" + year
    
    return render_template('reservations.html', final_appointments=final_appointments, final_date=final_date, date=date)


@app.route('/reservations')
def reservations():
    """Add reservations to the database """

    if "user" in session:
        user_id = session["user"]

    date_str = request.args.get('date_str') 
    time_str = request.args.get('time_str')

    print(time_str)
    print(date_str)


    appointment = crud.create_appointment(user_id, date_str, time_str)
    db.session.add(appointment)
    db.session.commit()
    flash("Your Appointment was scheduled!")

   

    return redirect('/homepage')


@app.route("/user_reservations")
def user_reservations():

    if "user" in session:
        user_id = session["user"]


    user_appointments = crud.get_user_appointments(user_id)
    print(user_appointments)

    return render_template("user-reservation.html", user_appointments=user_appointments)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)