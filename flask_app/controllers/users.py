import datetime
import math
import random
import smtplib
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.genre import Genre
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from .env import ADMINEMAIL
from .env import PASSWORD


@app.route('/')
def index():
    if 'user_id' in session:
        data = {
        'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        if user['is_verified'] == 0:  
            return redirect('/verify/email')
        return redirect('/dashboard')
    return redirect('/logout')

@app.route('/dashboard')
def dashboard():
    if 'user_id'in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('dashboard.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/registerpage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    data1 = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    if User.get_user_by_email(data1):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    #Validate the user
    if not User.validate_user(data1):
        return redirect(request.referrer)
    
    string = '0123456789ABCDEFGHIJKELNOPKQSTUV'
    vCode = ""
    length = len(string)
    for i in range(6) :
        vCode += string[math.floor(random.random() * length)]
    verification_code = vCode
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'verification_code': verification_code,
        'is_verified': 0,
        'admin': 0
    }

    User.create_user(data)

    LOGIN = ADMINEMAIL
    TOADDRS  = data['email']
    SENDER = ADMINEMAIL
    SUBJECT = 'Verify Your Email'
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
        % ((SENDER), "".join(TOADDRS), SUBJECT) )
    msg += f'Please use this verification code to activate your account: {verification_code}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(SENDER, TOADDRS, msg)
    server.quit()

    return redirect('/verify/email')


@app.route('/loginpage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods = ['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    data1 = {
        'email': request.form['email']
    }
    user = User.get_user_by_email(data1)
    #Checks if there is a user with that email
    if not user:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    #Checks if there is a user with that email
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/verify/email')
def verifyEmail():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['is_verified'] == 1:
        return redirect('/')
    return render_template('verifyEmail.html', loggedUser = user)

@app.route('/activate/account', methods=['POST'])
def activateAccount():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['is_verified'] == 1:
        return redirect('/dashboard')
    verificationCode = request.form['1'] + request.form['2'] + request.form['3'] + request.form['4'] + request.form['5'] + request.form['6']
    if len(verificationCode) < 1 :
        flash('Verification Code is required', 'blank')
        return redirect(request.referrer)
    if verificationCode != user['verification_code']:

        string = '0123456789ABCDEFGHIJKELNOPKQSTUV'
        vCode = ""
        length = len(string)
        for i in range(6) :
            vCode += string[math.floor(random.random() * length)]
        verification_code = vCode
        dataUpdate = {
            'verification_code': verification_code,
            'user_id': session['user_id']
        }

        User.updateVerificationCode(dataUpdate)
        LOGIN = ADMINEMAIL
        TOADDRS  = user['email']
        SENDER = ADMINEMAIL
        SUBJECT = 'Verify Your Email'
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'Use this verification code to activate your account: {verification_code}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()
        
        flash('Verification Code is wrong. We just sent you a new one', 'wrongCode')
        return redirect(request.referrer)
    User.activateAccount(data)
    return redirect('/dashboard')


@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': id
    }
    return render_template('profile.html', user = User.get_user_by_id(data))


@app.route('/editprofile')
def editProfile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('editProfile.html', loggedUser = User.get_user_by_id(data))

@app.route('/edit/user/profile', methods=['POST'])
def edit_user():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_user_on_update(request.form):
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        User.edit_user(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/deleteprofile')
def deleteProfile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        Job.delete_all_user_jobs(data)
        User.delete_user(data)
        return redirect('/logout')
    return redirect(request.referrer)


@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['is_verified'] == 1:
        return render_template('createPost.html', loggedUser = User.get_user_by_id(data))
    return redirect('verify/email')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginpage')
