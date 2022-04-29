from model import db, User, Appointment, connect_to_db


def create_user(username):
    """ Create and return a user """

    user = User(username=username)

    return user


def create_appointment(user_id, date_str, time_str, time_str2):
    """create an appointment for tasting melons """

    appointment = Appointment(user_id=user_id, date_str=date_str, time_str=time_str,time_str2 =time_str2)

    return appointment

def get_user_by_username(username):
    """ Return user id by user email"""

    user = User.query.filter(User.username==username).first()

    return user

def get_user_id_by_username(username):
    """ Return user id by user email"""

    user = User.query.filter(User.username==username).first()

    return user.user_id

def get_all_appointments_by_date(date_str):
    """Return all users """

    all_appointments = Appointment.query.filter_by(date_str=date_str).all()

    return all_appointments

def get_user_appointments(user_id):
    """ returns user appoinments """

    appointments = Appointment.query.filter_by(user_id=user_id).all()

    return appointments 
