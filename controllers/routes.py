from flask import render_template, request, redirect, url_for, session
from app import app


@app.route('/')
def home_page():
    return render_template('/Before_login_part/home_page.html')

@app.route('/pricing')
def pricing():
    return render_template("/Before_login_part/pricing_page.html")

@app.route('/contact')
def contact_page():
    return render_template("/Before_login_part/contact.html")

@app.route('/login')
def login_page():
    return render_template("/Before_login_part/login.html")