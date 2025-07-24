from flask import render_template, request, redirect, url_for, session, flash, jsonify
from models.models import db, User, ParkingLot, ParkingSpot, Reservation, Doubt, Newsletter
from app import app
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo

timezone = ZoneInfo("Asia/Kolkata")
def current_timestamp():
    return datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

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
                flash("Welcome Admin!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                flash("You have logged in successfully!", "success")
                return redirect(url_for('city_selection'))
        
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

            flash('You have registered Successfully! Please login to continue', 'success')
            return redirect(url_for('login_page'))

@app.route('/careers', methods=['GET', 'POST'])
def careers_page():
    if request.method == 'GET':
        return render_template('/Before_login_part/careers.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Email is required.', 'danger')
            return redirect(url_for('careers_page'))
        else:
            newsletter = Newsletter(email=email)
            db.session.add(newsletter)
            db.session.commit()
            flash('Thank you for subscribing to our newsletter!', 'success')
            return redirect(url_for('careers_page'))

@app.route('/affiliate', methods=['GET', 'POST'])
def affiliate_page():
    if request.method == 'GET':
        return render_template('/Before_login_part/affiliate.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Email is required.', 'danger')
            return redirect(url_for('careers_page'))
        else:
            newsletter = Newsletter(email=email)
            db.session.add(newsletter)
            db.session.commit()
            flash('Thank you for subscribing to our newsletter!', 'success')
            return redirect(url_for('affiliate_page'))

@app.route('/dashboard/admin', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        user = User.query.get(session['user_id'])
        lots = ParkingLot.query.all()
        return render_template(
            '/after_login_part/admin_side/admin_dashboard.html',
            user=user,
            lots=lots
        )

    elif request.method == 'POST':
        if request.form['form_type'] == 'add_lot':
            try:
                lotName = request.form.get('lotName')
                locationName = request.form.get('locationName')
                address = request.form.get('address')
                pincode = request.form.get('pincode')
                parkLitecount = int(request.form.get('parkLiteCount', 0) or 0)
                parkSmartCount = int(request.form.get('parkSmartCount', 0) or 0)
                parkProCount = int(request.form.get('parkProCount', 0) or 0)
                ratings = request.form.get('ratings', None)

                newLot = ParkingLot(
                    lotName=lotName,
                    locationName=locationName,
                    address=address,
                    pincode=pincode,
                    parkLiteCount=parkLitecount,
                    parkSmartCount=parkSmartCount,
                    parkProCount=parkProCount,
                    ratings=ratings
                )

                db.session.add(newLot)
                db.session.commit()

                spots = []
                for _ in range(parkLitecount):
                    spots.append(ParkingSpot(lot_id=newLot.id, type=1))
                for _ in range(parkSmartCount):
                    spots.append(ParkingSpot(lot_id=newLot.id, type=2))
                for _ in range(parkProCount):
                    spots.append(ParkingSpot(lot_id=newLot.id, type=3))

                db.session.add_all(spots)
                db.session.commit()

                if request.accept_mimetypes['application/json']:
                    return jsonify({
                        'id': newLot.id,
                        'address': newLot.address,
                        'pincode': newLot.pincode,
                        'parkLiteCount': newLot.parkLiteCount,
                        'parkSmartCount': newLot.parkSmartCount,
                        'parkProCount': newLot.parkProCount,
                        'ratings': newLot.ratings
                    })

                flash('Parking Lot added successfully.', 'success')
                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                db.session.rollback()
                if request.accept_mimetypes['application/json']:
                    return jsonify({'error': str(e)}), 500
                flash(f'Error adding Parking Lot: {str(e)}', 'danger')
                return redirect(url_for('admin_dashboard'))

        elif request.form['form_type'] == 'update-lot':
            id = request.form.get('id')
            lot = ParkingLot.query.get_or_404(id)
            return redirect(url_for('update_lot', lot_id=lot.id))

@app.route('/update/lot/<int:lot_id>', methods=['GET', 'POST'])
@admin_required
def update_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'GET':
        return render_template('/after_login_part/admin_side/search_lot.html', lot=lot)

    # POST request: update only the provided fields
    try:
        locationName = request.form.get('locationName')
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        # Parking counts (special handling because 0 is valid)
        parkLiteCount_raw = request.form.get('parkLiteCount')
        parkSmartCount_raw = request.form.get('parkSmartCount')
        parkProCount_raw = request.form.get('parkProCount')

        # Update only if provided
        if locationName:
            lot.locationName = locationName
        if address:
            lot.address = address
        if pincode:
            lot.pincode = pincode

        if parkLiteCount_raw != '' and parkLiteCount_raw is not None:
            lot.parkLiteCount = int(parkLiteCount_raw)
        if parkSmartCount_raw != '' and parkSmartCount_raw is not None:
            lot.parkSmartCount = int(parkSmartCount_raw)
        if parkProCount_raw != '' and parkProCount_raw is not None:
            lot.parkProCount = int(parkProCount_raw)

        # Commit updates
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        db.session.rollback()
        return redirect(url_for('update_lot', lot_id=lot_id))

@app.route('/delete/lot/<int:lot_id>', methods=['POST'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    
    db.session.delete(lot)
    db.session.commit()
    
    return redirect(url_for('admin_dashboard'))

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

@app.route('/admin/user/info', methods=['GET'])
@admin_required
def admin_user_info():
    email = request.args.get('email')
    if email:
        user = User.query.filter_by(emailId = email).first()
        if user:
            return render_template("/after_login_part/admin_side/user_info.html", user = user)
        else:
            return redirect(url_for('user_details'))

@app.route('/delete/user/<int:user_id>', methods = ["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user_details'))

@app.route("/city", methods=['GET','POST'])
@auth_required
def city_selection():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        return render_template('/after_login_part/user_side/users_after_login.html', user=user)
    else:
        city = request.form.get('city')
        session['selected_city'] = city
        return redirect(url_for('select_parkinglot', city = city))

@app.route('/select/parkinglot')
@auth_required
def select_parkinglot():
    city = session.get('selected_city')
    lot_list = ParkingLot.query.filter_by(locationName=city).all()
    return render_template('/after_login_part/user_side/lot_selction_list.html', lots=lot_list)

@app.route('/dashboard/user')
@auth_required
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    user = User.query.get(session['user_id'])
    city = session.get('selected_city')
    reservations = Reservation.query.filter_by(userId=user.id).all()

    for reservation in reservations:
        if reservation.parkingType == 1:
            reservation.parkingTypeName = "Park Lite"
        elif reservation.parkingType == 2:
            reservation.parkingTypeName = "Park Smart"
        elif reservation.parkingType == 3:
            reservation.parkingTypeName = "Park Pro"
        else:
            reservation.parkingTypeName = "Unknown"

    lite_count = sum(1 for reservation in reservations if reservation.parkingType == 1)
    smart_count = sum(1 for reservation in reservations if reservation.parkingType == 2)
    pro_count = sum(1 for reservation in reservations if reservation.parkingType == 3)
    return render_template('/after_login_part/user_side/user_dashboard.html', user=user, city=city, reservations = reservations, lite_count=lite_count, smart_count=smart_count, pro_count=pro_count)

@app.route('/user/edit/profile', methods = ["GET", "POST"])
@auth_required
def edit_user_profile():
    if request.method == "GET":
        return render_template("/after_login_part/user_side/edit_profile_user.html")
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

        return redirect(url_for('user_dashboard'))

@app.route('/book/parkou/<int:lot_id>', methods=['GET', 'POST'])
@auth_required
def book_parkou(lot_id):
    if request.method == 'GET':
        lot = ParkingLot.query.get(lot_id)
        spots = ParkingSpot.query.filter(ParkingSpot.lot_id == lot_id).all()
        total_lite = sum(1 for spot in spots if spot.type == 1)
        total_smart = sum(1 for spot in spots if spot.type == 2)
        total_pro = sum(1 for spot in spots if spot.type == 3)
        available_lite = sum(1 for spot in spots if not spot.occupied and (spot.type == 1))
        available_smart = sum(1 for spot in spots if not spot.occupied and (spot.type == 2))
        available_pro = sum(1 for spot in spots if not spot.occupied and (spot.type == 3))
        return render_template('/after_login_part/user_side/booking_page.html',
                                lot = lot, 
                                spots = spots,
                                total_lite = total_lite,
                                total_smart = total_smart,
                                total_pro = total_pro,
                                available_lite = available_lite,
                                available_smart = available_smart,
                                available_pro = available_pro)
    if request.method == 'POST':
        if request.form['form_type'] == 'park_lite':
            spot_id = request.form.get('spot_id')
            timestamp = current_timestamp()
            user_id = session['user_id']
            spot = ParkingSpot.query.get(spot_id)

            if spot and not spot.occupied and spot.type == 1:
                reservation = Reservation(
                    spotId=spot.id,
                    userId=user_id,
                    parkingType = spot.type,
                    parkingTimestamp=timestamp,
                    leavingTimestamp="", 
                    parkingCost=0,
                    ratings=None
                )
                spot.occupied = True
                db.session.add(reservation)
                db.session.commit()
                flash('Parking Spot booked successfully!', 'success')
            else:
                flash('Selected parking spot is not available.', 'danger')
            return redirect(url_for('booking_status', reservation_id=reservation.id))
        if request.form['form_type'] == 'park_smart':
            spot_id = request.form.get('spot_id')
            timestamp = current_timestamp()
            user_id = session['user_id']
            spot = ParkingSpot.query.get(spot_id)

            if spot and not spot.occupied and spot.type == 2:
                reservation = Reservation(
                    spotId=spot.id,
                    userId= user_id,
                    parkingType = spot.type,
                    parkingTimestamp=timestamp,
                    leavingTimestamp="", 
                    parkingCost=0,
                    ratings=None
                )
                spot.occupied = True
                db.session.add(reservation)
                db.session.commit()
                flash('Parking Spot booked successfully!', 'success')
            else:
                flash('Selected parking spot is not available.', 'danger')
            return redirect(url_for('booking_status', reservation_id=reservation.id))

    return redirect(url_for('book_parkou', lot_id=lot_id))

def calculate_parking_cost(parking_timestamp, leaving_timestamp, spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if not spot:
        return 0

    if spot.type == 1:
        rate_per_hour = 60
    elif spot.type == 2:
        rate_per_hour = 90
    elif spot.type == 3:
        rate_per_hour = 150
    else:
        return 0

    parking_time = datetime.strptime(parking_timestamp, '%Y-%m-%d %H:%M:%S')
    leaving_time = datetime.strptime(leaving_timestamp, '%Y-%m-%d %H:%M:%S')
    duration = (leaving_time - parking_time).total_seconds() / 3600

    return max(0, int(duration * rate_per_hour))

@app.route('/booking/status/<int:reservation_id>', methods = ['GET', 'POST'])
@auth_required
def booking_status(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if request.method == 'GET':
        return render_template('/after_login_part/user_side/booking_status.html', reservation=reservation)

    elif request.method == 'POST':
        if reservation:
            leaving_timestamp = current_timestamp()
            reservation.leavingTimestamp = leaving_timestamp
            reservation.parkingCost = calculate_parking_cost(reservation.parkingTimestamp, leaving_timestamp, reservation.spotId)
            reservation.ratings = ""
            spot = ParkingSpot.query.get(reservation.spotId)
            spot.occupied = False
            db.session.commit()
            
        return redirect(url_for('ratings', reservation_id=reservation.id))

@app.route('/ratings/<int:reservation_id>', methods=['GET', 'POST'])
@auth_required
def ratings(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if request.method == 'GET':
        parking_timestamp = reservation.parkingTimestamp
        leaving_timestamp = reservation.leavingTimestamp
        cost = reservation.parkingCost
        reservationtype = reservation.parkingType
        if reservationtype == 1:
            reservationtype = "Park Lite"
        elif reservationtype == 2:
            reservationtype = "Park Smart"
        elif reservationtype == 3:
            reservationtype = "Park Pro"
        return render_template('/after_login_part/user_side/ratings.html', reservation=reservation, parking_timestamp=parking_timestamp, leaving_timestamp=leaving_timestamp, cost=cost, reservationtype=reservationtype)

    elif request.method == 'POST':
        ratings = request.form.get('ratings')
        reservation.ratings = ratings
        db.session.commit()
        return redirect(url_for('user_dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login_page'))