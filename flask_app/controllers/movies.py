from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.genre import Genre
from datetime import datetime
import os
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

# Check if the format is right 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dashboard')
def dashboard():
    if 'user_id'in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('dashboard.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/job', methods = ['POST'])
def createJob():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'salary': request.form['salary'],
        'user_id': session['user_id']
    }
    if not Job.validate_job(data):
        return redirect(request.referrer)
    Job.create_job(data)
    return redirect('/')


@app.route('/create/proposal', methods = ['POST'])
def createProposal():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'skill1': request.form['skill1'],
        'skill2': request.form['skill2'],
        'skill3': request.form['skill3'],
        'user_id': session['user_id']
    }   
    if not Proposal.validate_proposal(data):
        return redirect(request.referrer)
    Proposal.create_proposal(data)
    return redirect(request.referrer)

@app.route('/jobproposals')
def jobProposal():
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id']
        }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/')
    return render_template('jobproposals.html', loggedUser=loggedUser, jobs = Job.get_jobs(), proposals = Proposal.get_proposals())


@app.route('/job/<int:id>')
def viewJob(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'job_id': id
    }
    loggedUser = User.get_user_by_id(data)
    job = Job.get_job_by_id(data)
    creator_id = job['user_id']
    userid = {
        'user_id': creator_id
    }
    return render_template('view.html', job = job, loggedUser = loggedUser, creator = User.get_user_by_id(userid))
