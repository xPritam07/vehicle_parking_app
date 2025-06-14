from flask import render_template, request, redirect, url_for, session, flash
from models.models import db, User, ParkingLot, ParkingSpot, Reservation, Doubt
from app import app
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash



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


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == "GET":
        return render_template('/Before_login_part/home_page.html')

    else:
        name = request.form.get('name')
        email = request.form.get('email')
        question = request.form.get('question')

        doubt = Doubt(name=name,email=email,question=question)

        db.session.add(doubt)
        db.session.commit()
    
        return render_template("/Before_login_part/home_page.html")
    
@app.route('/pricing')
def pricing():
    return render_template("/Before_login_part/pricing_page.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == "GET":
        return render_template("/Before_login_part/contact.html")
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        question = request.form.get('question')

        doubt = Doubt(name=name,email=email,question=question)

        db.session.add(doubt)
        db.session.commit()
    
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

            if not user:
                flash("User does not exist.")
                return redirect(url_for('login_page'))
            if not user.check_password(password):
                flash("Incorrect password.", "danger")
                return redirect(url_for('login_page'))
            
            session['user_id'] = user.id

            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        
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

@app.route('/dashboard/admin')
@admin_required
def admin_dashboard():
    user = User.query.get(session['user_id'])
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('/after_login_part/admin_side/admin_dashboard.html', user = user)

@app.route('/admin/doubts')
@admin_required
def doubt_page():
    doubts = Doubt.query.all()
    return render_template('/after_login_part/admin_side/doubt_page.html', doubts=doubts)


@app.route('/doubt/delete/<int:doubt_id>', methods = ['POST'])
@admin_required
def delete_doubt(doubt_id):
    doubt = Doubt.query.get_or_404(doubt_id)

    db.session.delete(doubt)
    db.session.commit()

    return redirect(url_for('doubt_page'))

@app.route('/admin/doubt/reply/<int:doubt_id>')
@admin_required
def doubt_reply(doubt_id):
    doubt = Doubt.query.get_or_404(doubt_id)

    return render_template("/after_login_part/admin_side/mail_page.html", doubt = doubt)

@app.route('/back')
@admin_required
def return_back():
    return redirect(url_for('doubt_page'))

@app.route('/admin/user/info', methods=['GET'])
@admin_required
def admin_user_info():
    email = request.args.get('email')
    user = None
    if email:
        user = User.query.filter_by(emailId = email).first()
    return render_template("/after_login_part/admin_side/user_info.html", user = user)


@app.route('/admin/edit/profile', methods = ["GET", "POST"])
@admin_required
def edit_admin_profile():
    if request.method == "GET":
        return render_template("/after_login_part/admin_side/edit_profile.html")
    else:
        name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        passhash = generate_password_hash(password, method='pbkdf2:sha256')

        user = User.query.get(session['user_id'])

        user.fullName = name
        user.emailId = email
        user.passhash = passhash

        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    
@app.route("/admin/user")
@admin_required
def user_details():
    users = User.query.all()
    return render_template('/after_login_part/admin_side/user_details.html', users = users)

@app.route("/dashboard/user")
@auth_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    return render_template('/after_login_part/user_side/user_dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login_page'))