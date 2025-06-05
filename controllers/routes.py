from flask import render_template, request, redirect, url_for, session, flash
from models.models import db, User, ParkingLot, ParkingSpot, Reservation, Doubt
from app import app
from functools import wraps


def auth_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue")
            return redirect(url_for('login_page'))
        return func(*args,**kwargs)
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if "user_id" not in session:
            return redirect(url_for('login_page'))
        user=User.query.get(session['user_id'])
        if not user.is_admin:
            flash('You are not a authorized personel')
            return redirect(url_for('login_page'))
        return func(*args,**kwargs)
    return inner


@app.route('/')
def home_page():
    return render_template('/Before_login_part/home_page.html')

@app.route('/pricing')
def pricing():
    return render_template("/Before_login_part/pricing_page.html")

@app.route('/contact')
def contact_page():
    return render_template("/Before_login_part/contact.html")

@app.route('/about')
def about_page():
    return render_template('/Before_login_part/about_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("/Before_login_part/login.html")

    else:
        form_type = request.form.get('form-type')

        if form_type == "login":
            emailId = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(emailId=emailId).first()

            if emailId == '' or password == '':
                return flash("Email or Password can not be empty.", "danger")
            if not user:
                flash("User does not exist.")
                return redirect(url_for('login_page'))
            return redirect(url_for('#'))
        
        elif form_type == 'register':
            fullName = request.form.get('fullName')
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(emailId = email).first()

            if user:
                flash("Email alrady registered!", 'danger')
                return redirect(url_for('login_page'))
            
            newUser = User(fullName = fullName, emailId = email, password = password)
            db.session.add(newUser)
            db.session.commit()

            flash('Successful registration!', 'success')
            return redirect(url_for('login_page'))