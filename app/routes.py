from flask import render_template,redirect,request,url_for,flash,abort
from app import app,mail

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about():
    return render_template('about_us.html', title='About us')

@app.route('/our_products_&_services')
def products():
    return render_template('our_products&services.html', title='Our products and services')

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html', title='Contact us')