import email
from nis import cat
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from flask import request,redirect,url_for
from flask import Blueprint
from flask import render_template,request,flash
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash



auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])  
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in Successfully.',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password/email.',category='error')
        else:
            flash('User not found.',category='error')

    return redirect(url_for('views.home',user=current_user))

#logout function

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#register function

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method =="POST":
        firstName = request.form.get('fname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists',category='error')
        elif firstName == "":
            flash('Please enter your first name',category='error')
        
        
        elif len(email) < 4:
            flash('Email must be longer than 3 characters',category='error')
        elif len(password1) < 8:
            flash('Password length must be longer than 7 characters',category='error')
        elif password2 == "":
            flash('Please confirm your password',category='error')
        elif password1 != password2 :
            flash('The two passwords do not match',category='error')
        else:

            #add user to the db
            new_user = User(email=email,first_name=firstName,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully',category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('signup.html',user=current_user)