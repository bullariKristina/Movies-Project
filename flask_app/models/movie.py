from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Movie():
    db_name = 'movies_db'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.rating = data['rating']
        self.release_date = data['release_date']
        self.run_time = data['run_time']
        self.poster_pic = data['poster_pic']
        self.user_id = data['user_id']
        self.in_theater = data['in_theater']
        self.trailer = data['trailer']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_movie(cls, data):
        query = "INSERT INTO movies (title, description, rating, release_date, run_time, poster_pic, user_id, in_theater, trailer) VALUES ( %(title)s, %(description)s, %(rating)s, %(release_date)s, %(run_time)s, %(poster_pic)s, %(user_id)s, 0, %(trailer)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one_movie(cls, data):
        query = 'SELECT MAX(movies.poster_pic) AS poster_pic, MAX(movies.id) AS id, movies.title AS title, MAX(movies.description) AS description, MAX(movies.rating) AS rating, MAX(movies.release_date) AS release_date, MAX(movies.run_time) AS run_time, GROUP_CONCAT(genres.genre_name) AS movie_genres FROM movies LEFT JOIN genres ON movies.id = genres.movie_id WHERE movies.id = %(movie_id)s GROUP BY movies.title ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_movies(cls):
        try:
            query = 'SELECT * FROM movies;'
            results = connectToMySQL(cls.db_name).query_db(query)
            if results:
                return results
            else:
                return []
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
        
    @classmethod
    def get_movie_by_id(cls, data):
        query = 'SELECT * FROM movies WHERE id= %(movie_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_last_movie(cls):
        query = 'SELECT * FROM movies ORDER BY created_at DESC LIMIT 1;'
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_last_movies(cls):
        query = 'SELECT * FROM movies ORDER BY created_at DESC;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies = []
        if results:
            for movie in results:
                movies.append(movie)
            return movies
        return movies
    
    @classmethod
    def get_4_last_movies(cls):
        query = 'SELECT * FROM movies ORDER BY created_at DESC LIMIT 4;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies = []
        if results:
            for movie in results:
                movies.append(movie)
            return movies
        return movies
    
    @classmethod
    def get_last_movies_intheater(cls):
        query = 'SELECT * FROM movies where movies.in_theater = 1 ORDER BY created_at DESC LIMIT 8;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies = []
        if results:
            for movie in results:
                movies.append(movie)
            return movies
        return movies
    
    @classmethod
    def get_movie_search(cls, data):
        query = 'SELECT * FROM movies WHERE movies.title LIKE %(movie_name)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def add_in_theater(cls, data):
        query = 'UPDATE movies SET in_theater = 1 WHERE movies.id = %(movie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def remove_from_theater(cls, data):
        query = 'UPDATE movies SET in_theater = 0 WHERE movies.id = %(movie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_movies_intheater(cls):
        query = 'SELECT * FROM movies where movies.in_theater = 1;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies= []
        if results:
            for movie in results:
                movies.append(movie)
            return movies
        return movies
    
    @classmethod
    def get_4_movies_intheater(cls):
        query = 'SELECT * FROM movies where movies.in_theater = 1 LIMIT 4;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies= []
        if results:
            for movie in results:
                movies.append(movie)
            return movies
        return movies
    @classmethod
    def delete_all_user_movies(cls, data):
        query = "DELETE FROM movies WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def comment(cls, data):
        query = "INSERT INTO comments (movie_id, user_id) VALUES (%(movie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (movie_id, user_id) VALUES (%(movie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE movie_id = %(movie_id)s and user_id = %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def get_movie_likers(cls, data):
        query = "SELECT * from likes LEFT JOIN users on likes.user_id = users.id WHERE movie_id = %(movie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfLikes = []
        if results:
            for row in results:
                nrOfLikes.append(row['id'])
            return nrOfLikes
        return nrOfLikes
    
    @classmethod
    def get_num_likes(cls, data):
        query = "SELECT COUNT(*) AS num_likes FROM likes WHERE likes.movie_id = %(movie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]['num_likes']
        return 0
    

    


    @staticmethod
    def validate_movie(data):
        is_valid = True
        if len(data['title'])<2:
            flash('Title must be more than 2 characters', 'movieTitle')
            is_valid = False
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'movieDescription')
            is_valid = False 
        if not data['rating']:
            flash('Please do not leave this blank', 'movieRating')
            is_valid = False
        if not data['release_date']:
            flash('Please do not leave this blank', 'movieReleaseDate')
            is_valid = False
        if not data['run_time']:
            flash('Please do not leave this blank', 'movieRunTime')
            is_valid = False
        return is_valid