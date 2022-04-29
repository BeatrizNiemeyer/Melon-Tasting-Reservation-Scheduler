from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User table"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)

    apt = db.relationship("Appointment", back_populates="user")
   

class Appointment(db.Model):
    """Appointments table"""

    __tablename__ = "appointments"

    apt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date_str = db.Column(db.String)
    time_str = db.Column(db.String)
    time_str2 = db.Column(db.String) 
    
    user = db.relationship("User", back_populates="apt")

def connect_to_db(flask_app, db_uri="postgresql:///mtr_data", echo=False):
    """Conecting to db"""
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

def example_data():
    """ Create example data for the test database"""

    user_1 = User(username='beatriz')
    
    db.session.add(user_1)
    db.session.commit()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)