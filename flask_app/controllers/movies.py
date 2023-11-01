from flask_app import app

from flask import render_template, redirect, session, request, flash ,url_for

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create/movie', methods = ['POST'])
def createMovie():
    if 'user_id' in session:
        if not Movie.validate_movie(request.form):
            return redirect(request.referrer)
        if not request.files['poster_pic']:
            flash('Image is required!', 'posterImage')
            return redirect(request.referrer)
   
        image = request.files['poster_pic']
        if not '.' in image.filename and \
           image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            flash('Image should be in png, jpg, jpeg format!', 'postImage')
            return redirect(request.referrer)
        
        if image:
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        data = {
            'title': request.form['title'],
            'trailer': request.form['trailer'],
            'description': request.form['description'],
            'rating': request.form['rating'],
            'release_date': request.form['release_date'],
            'run_time': request.form['run_time'],
            'poster_pic': filename1,
            'user_id': session['user_id']
            }
        Movie.create_movie(data)
        
        return redirect('/addgenre')
    return redirect('/')


@app.route('/addgenre')
def add_genre():
    if 'user_id' not in session:
            return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('genre.html', loggedUser = User.get_user_by_id(data), movie = Movie.get_last_movie())


@app.route('/add/genre', methods = ['POST'])
def addGenre():
    if 'user_id' not in session:
        return redirect('/')
    movie =  Movie.get_last_movie()
    data = {
        'genre_name': request.form['genre_name'],
        'movie_id': movie['id']
    }   
    Genre.create_genre(data)
    return redirect('/addgenre')


@app.route('/movie/<int:id>')
def viewMovie(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'movie_id': id
    }
    loggedUser = User.get_user_by_id(data)
    movie = Movie.get_movie_by_id(data)
    creator_id = movie['user_id']
    userid = {
        'user_id': creator_id
    }
    return render_template('movie.html', movie = movie, loggedUser = loggedUser, creator = User.get_user_by_id(userid))

@app.route('/comment/<int:id>')  #id of movie
def comment(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'comment': request.form['comment'],
        'user_id': session['user_id'],
        'movie_id': id
    }
    User.comment(data)
    return redirect(request.referrer())

@app.route('/in/theater')
def in_Theater():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('in_theater.html', loggedUser = User.get_user_by_id(data), theaterMovies = Movie.get_all_movies_intheater())


@app.route('/latest/movies')
def latestMovies():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('in_theater.html', loggedUser = User.get_user_by_id(data), theaterMovies = Movie.get_last_movies())

@app.route('/search',  methods=['POST'])
def search():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'movie_name': request.form['movie_name'],
        'user_id': session['user_id']
    }
    movie = Movie.get_movie_search(data)
    if movie:
        return render_template('movie.html', movie = movie, loggedUser = User.get_user_by_id(data)) 
    return render_template('not_found.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['admin'] == 1:
        return render_template('admin.html', loggedUser = loggedUser, movies = Movie.get_movies())
    return redirect('/')

@app.route('/add/in/theater/<int:id>')
def addTheater(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'movie_id': id
    }
    moviesTheater = Movie.get_all_movies_intheater()
    if 'movie_id' not in moviesTheater:
        Movie.add_in_theater(data)
    return redirect(request.referrer)

@app.route('/remove/theater/<int:id>')
def removeTheater(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'movie_id': id
    }
    Movie.remove_from_theater(data)
    return redirect(request.referrer)
    
    