import os
import secrets
from PIL import Image
from flask import render_template,redirect,request,url_for,flash,abort
from app import app,mail,bcrypt,db
from app.forms import (RequestQuoteForm,LoginForm,UpdateAccountForm,RequestResetForm,
ResetPasswordForm,AddCareerForm,UpdateCareerForm,CompanyDetailsResetForm)
from flask_mail import Message
from app.models import Users,Careers,Company,ContactDetails
from flask_login import login_user,current_user,logout_user,login_required



def send_email(email,message,phonenumber,fullname,producttype):
    msg = Message(f'Email from {email}, phone number: {phonenumber}', 
                   sender=email,
                   recipients=['smuminaetx100@gmail.com'])
    msg.body = f'''
Company name/Individual: {fullname}
Product type: {producttype}
{message}
'''
    mail.send(msg)

@app.route('/', methods = ['GET','POST'])
def index():
    company = Company.query.all()
    contacts = ContactDetails.query.all()
    form = RequestQuoteForm()
    if form.validate_on_submit():
        send_email(email=form.email.data,phonenumber=form.phonenumber.data,
        fullname=form.fullname.data,message=form.message.data,producttype=form.producttype.data)
        flash('Email has been send','info')
    return render_template('index.html', form = form, company=company,contacts=contacts)

@app.route('/about_us')
def about():
    return render_template('about_us.html', title='About us')

@app.route('/our_products_&_services')
def products():
    return render_template('our_products&services.html', title='Our products and services')

@app.route('/contact_us', methods=['GET','POST'])
def contact():
    form = RequestQuoteForm()
    if form.validate_on_submit():
        send_email(email=form.email.data,phonenumber=form.phonenumber.data,
        fullname=form.fullname.data,message=form.message.data,producttype=form.producttype.data)
        flash('Email has been send','info')
    return render_template('contact_us.html', title='Contact us', form=form)

@app.route('/career_section')
def careers():
    careers = Careers.query.all()
    return render_template('careers.html',careers=careers)

@app.route('/admin_login', methods = ['GET','POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash('You have been successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_home'))
        else:
            flash('Email or password incorrect!','danger')
    return render_template('admin/admin_login.html', title = 'Login', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin_login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

@app.route('/admin')
@login_required
def admin_home():
    if current_user.admin == False:
        abort(403)
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/admin_home.html', profile_pic=image_file)

@app.route('/account', methods = ['GET','POST'])
@login_required
def account():
    if current_user.admin == False:
        return redirect(url_for('index'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/admin_account.html', title = current_user.username, profile_pic = image_file, form = form)

@app.route('/admin_careers', methods=['GET','POST'])
@login_required
def admin_careers():
    if current_user.admin == False:
        abort(403)
    careers = Careers.query.all()
    form = AddCareerForm()
    if form.validate_on_submit():
        career = Careers(name=form.name.data,description=form.description.data)
        db.session.add(career)
        db.session.commit()
        flash('New career has been added successfully','info')
        return redirect(url_for('admin_careers'))
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/admin_careers.html', careers=careers,form=form, profile_pic = image_file)

@app.route('/update_career/<int:id>',methods=['GET','POST'])
@login_required
def update_career(id):
    if current_user.admin == False:
        abort(403)

    form = UpdateCareerForm()
    if form.validate_on_submit():
        career = Careers.query.get_or_404(str(id))
        if career:
            career.name = form.name.data
            career.description = form.description.data
            db.session.commit()
            flash('Career info has been updated!', 'success')
            return redirect(url_for('admin_careers'))
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/admin_update_career.html', form = form,profile_pic = image_file)
    
@app.route('/delete_career/<int:id>')
@login_required
def delete_career(id):
    if current_user.admin == False:
        abort(403)
    career = Careers.query.get_or_404(str(id))
    db.session.delete(career)
    db.session.commit()
    flash('Career has been deleted!', 'success')
    return redirect(url_for('admin_careers'))



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                   sender='smuminaetx100@gmail.com',
                   recipients=[user.email])
    msg.body = f'''To reset your password, click the link below:
{url_for('reset_token',token=token,_external = True)}
Token expires within one hour!
If you did not make this request simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route('/reset_password/<token>', methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login and access your account', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if current_user.admin == False:
        abort(403)
    company = Company.query.all()
    contacts = ContactDetails.query.all()
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/settings.html', title='Settings',company=company,contacts=contacts,profile_pic=image_file)

@app.route('/Update_mission',methods=['GET','POST'])
@login_required
def update_mission():
    if current_user.admin == False:
        abort(403)
    company = Company.query.first_or_404()
    form = CompanyDetailsResetForm()
    if form.validate_on_submit():
        company.mission = form.details.data
        db.session.commit()
        flash('Company mission updated','success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.details.data = company.mission
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/update_mission.html', title='Update mission',form=form,profile_pic=image_file)

@app.route('/Update_vision',methods=['GET','POST'])
@login_required
def update_vision():
    if current_user.admin == False:
        abort(403)
    company = Company.query.first_or_404()
    form = CompanyDetailsResetForm()
    if form.validate_on_submit():
        company.vision = form.details.data
        db.session.commit()
        flash('Company vision updated','success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.details.data = company.vision
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/update_vision.html', title='Update vision',form=form,profile_pic=image_file)

@app.route('/Update_focus',methods=['GET','POST'])
@login_required
def update_focus():
    if current_user.admin == False:
        abort(403)
    company = Company.query.first_or_404()
    form = CompanyDetailsResetForm()
    if form.validate_on_submit():
        company.company_focus = form.details.data
        db.session.commit()
        flash('Company focus updated','success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.details.data = company.company_focus
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/update_focus.html', title='Update focus',form=form,profile_pic=image_file)

@app.route('/Update_phone_number',methods=['GET','POST'])
@login_required
def update_phone():
    if current_user.admin == False:
        abort(403)
    contacts = ContactDetails.query.first_or_404()
    form = CompanyDetailsResetForm()
    if form.validate_on_submit():
        contacts.phone_number = form.details.data
        db.session.commit()
        flash('Phone number details updated','success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.details.data = contacts.phone_number
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/update_focus.html', title='Update phone number',form=form,profile_pic=image_file)

@app.route('/Update_email',methods=['GET','POST'])
@login_required
def update_email():
    if current_user.admin == False:
        abort(403)
    contacts = ContactDetails.query.first_or_404()
    form = CompanyDetailsResetForm()
    if form.validate_on_submit():
        contacts.email = form.details.data
        db.session.commit()
        flash('Email address details updated','success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.details.data = contacts.email
    image_file = url_for('static', filename = 'images/profile_pics/' + current_user.profile_pic)
    return render_template('admin/update_focus.html', title='Update email',form=form,profile_pic=image_file)