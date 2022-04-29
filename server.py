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

#These are the appointment times. Appointments are made every 30min, 24hours a day!!
times = ["00:30", "01:00", "01:30" ,"02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00",
"06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", 
"13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", 
"19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "00:00" ]

times_dict = {"12:30AM": "00:30", "01:00AM":"01:00", "01:30AM":"01:30" ,"02:00AM":"02:00", "02:30AM":"02:30", "03:00AM":"03:00", 
"03:30AM":"03:30", "04:00AM":"04:00", "04:30AM":"04:30", "05:00AM":"05:00", "05:30AM":"05:30", "06:00AM":"06:00",
"06:30AM":"06:30", "07:00AM":"07:00", "07:30AM":"07:30", "08:00AM":"08:00", "08:30AM":"08:30", "09:00AM":"09:00", 
"09:30AM":"09:30", "10:00AM":"10:00", "10:30AM":"10:30", "11:00AM":"11:00", "11:30AM":"11:30", "12:00PM":"12:00", 
"12:30PM":"12:30", "1:00PM":"13:00", "1:30PM":"13:30", "2:00PM":"14:00", "2:30PM":"14:30", "3:00PM":"15:00", 
"3:30PM":"15:30", "4:00PM":"16:00", "4:30PM":"16:30", "5:00PM":"17:00", "5:30PM":"17:30", "6:00PM":"18:00", 
"6:30PM":"18:30", "7:00PM":"19:00", "7:30PM":"19:30", "8:00PM":"20:00", "8:30PM":"20:30", "9:00PM":"21:00",
"9:30PM":"21:30", "10:00PM":"22:00", "10:30PM":"22:30", "11:00PM":"23:00", "11:30PM":"23:30", "12:00AM":"00:00" }

@app.route("/")
def login_page():
    """Show homepage"""

    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    """ Login with username"""

    #Getting data from the form
    username = request.form.get('username')

    #Getting user from database, if they are registered
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

    #Getting data from the form
    date = request.form.get('date') 
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

  
    #The start and end time are in 24hours format. So in this for loop I am converting the start and end time in this format -> 14:30 to 1430 (now an integer), for example.
    # I am also converting the times inside my times list (the global variable) in this format
    #My approach here is, if start_date is 14:30 (1430) and my end_time is 18:45 (1845), I just will append the times between/equal the numbers 1430 and 1845 from my times list to the 
    #list_of_times list.

    list_of_times = []
    for time in times:
        if (int(start_time[:2] + start_time[3:])) <= (int(time[:2] + time[3:])) and (int(end_time[:2] + end_time[3:])) >= (int(time[:2] + time[3:])):
           list_of_times.append(time)

    
     

    #all_appointments is a variable storing all the times of appointments made in the date provided by user. So these times are already taken
    all_appointments = crud.get_all_appointments_by_date(date)


    #Now I am looping over all the appointments made in the date selected by user, and checking if the they already have an scheduled appointment por that day,
    #If they do, they are not able to make another appointment!
    for apt in all_appointments:
        if apt.user_id == user_id:
            flash("sorry, you already have an appointment that day!")
            return redirect('/homepage')


    list_of_unavailable_times =[]

    #Storing the "taken times" for selected day, in list_of_unavailable_times list.
    for apt in all_appointments:
        list_of_unavailable_times.append(apt.time_str)


    appointments_available = []

    #Looping over our list_of_times list, where contains all the appointments times in between start and end times selected by user, and checking if these times
    #are also in the list_of_unavailable_times. If not, that means that that time is available, so we will append it to appointments_available list.
    for time in list_of_times:
        if time not in list_of_unavailable_times and time not in appointments_available:
            appointments_available.append(time)

    final_appointments = []

    if appointments_available == []:
        flash("No appointments available int this day or time!")
        return redirect("/homepage")


    #This loop is simply converts the appointments available in 24hours format to 12hours format. So 14:30 now is 2:30PM. 
    for apt in appointments_available:
        if int(apt[:2]) < 12:
            time = apt + "AM"
        elif int(apt[:2]) == 12:
            time = apt + "PM"
        else:
            time = str(int(apt[:2]) - 12) + apt[2:] + "PM"
        final_appointments.append(time)
        
   
    #Converting the date from 2022-04-29 format to 04/29/2022 format.
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

    
    #Getting the date and available time selected by user.
    date_str = request.args.get('date_str') 
    time_str = request.args.get('time_str')

    #getting time in 24hour format
    time = times_dict[time_str]
    #Creating an appointment and saving it to the database.
    appointment = crud.create_appointment(user_id, date_str, time, time_str,)
    db.session.add(appointment)
    db.session.commit()
    flash("Your Appointment was scheduled!")

    return redirect('/homepage')


@app.route("/user_reservations")
def user_reservations():

    if "user" in session:
        user_id = session["user"]

    #Getting all the appointments made by the user, and displayed in the user user-reservation.html template
    user_appointments = crud.get_user_appointments(user_id)

    return render_template("user-reservation.html", user_appointments=user_appointments)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



