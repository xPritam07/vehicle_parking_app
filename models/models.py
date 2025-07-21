from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import app
from sqlalchemy import event
from sqlalchemy.engine import Engine
from datetime import datetime

db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(128), nullable = False, unique = False)
    emailId = db.Column(db.String(128), nullable = False, unique = True)
    passhash = db.Column(db.String(128), nullable = False, unique = False)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reservation = db.relationship('Reservation', cascade = "all, delete", passive_deletes = True, back_populates = 'user')


    @property
    def password(self):
        raise AttributeError('Password is secret')

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

class ParkingLot(db.Model):
    __tablename__ = "parkinglot"
    id = db.Column(db.Integer, primary_key = True)
    locationName = db.Column(db.String(128))
    address = db.Column(db.String(512), unique = True, nullable = False)
    pincode = db.Column(db.String(128), unique = True, nullable = False)
    parkLiteCount = db.Column(db.Integer)
    parkSmartCount = db.Column(db.Integer)
    parkProCount = db.Column(db.Integer)
    ratings = db.Column(db.Integer, default = 0)

    parkingspot = db.relationship('ParkingSpot', cascade = "all, delete", passive_deletes = True, back_populates = 'parkinglot')

class ParkingSpot(db.Model):
    __tablename__ = "parkingspot"
    id = db.Column(db.Integer, primary_key = True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parkinglot.id', ondelete = 'CASCADE'), nullable = False)
    type = db.Column(db.Integer, nullable = False)

    parkinglot = db.relationship('ParkingLot', back_populates='parkingspot')
    reservation = db.relationship('Reservation', cascade = "all, delete", passive_deletes = True, back_populates = 'parkingspot')


class Reservation(db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key = True)
    spotId = db.Column(db.Integer, db.ForeignKey("parkingspot.id", ondelete = "CASCADE"), nullable = False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id", ondelete = "CASCADE"),  nullable = False)
    parkingTimestamp = db.Column(db.String(128))
    leavingTimestamp = db.Column(db.String(128))
    parkingCost = db.Column(db.Integer)
    ratings = db.Column(db.Integer)

    user = db.relationship('User', back_populates='reservation')
    parkingspot = db.relationship('ParkingSpot', back_populates='reservation')


class Doubt(db.Model):
    __tablename__ = "doubts"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), nullable = False)
    question = db.Column(db.String(512), nullable = False)

with app.app_context(): 
    db.create_all()
    admin = User.query.filter_by(emailId='admin@gmail.com').first()
    if not admin:
        admin=User(emailId='admin@gmail.com',password='admin',fullName='admin',is_admin=True)
        db.session.add(admin)
        db.session.commit()