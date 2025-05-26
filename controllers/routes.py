from flask import render_template, request, redirect, url_for, session
from app import app




@app.route('/')
def home_page():
    return render_template('index.html')