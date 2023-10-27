from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Genre():
    db_name = 'movies_db'
    def __init__( self , data ):
        self.id = data['id']
        self.genre_name = data['genre_name']
        self.movie_id = data['movie_id']

    @classmethod
    def create_genre(cls, data):
        query = "INSERT INTO genres (genre_name, movie_id) VALUES (%(genre_name)s, %(movie_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    valid_genres = ["Action", "Adventure", "Comedy", "Drama", "Horror", "Science Fiction"]
    
    # @classmethod
    # def get_all_genres(cls):

    @staticmethod
    def validate_genre(data):
        if data['genre_name'] not in Genre.valid_genres:
            flash("This genre doesn't exist", 'genreName')
            is_valid = False
        

    
