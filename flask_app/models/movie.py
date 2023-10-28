from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Movie():
    db_name = 'movies_db'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.traile = data['trailer']
        self.rating = data['rating']
        self.release_date = data['release_date']
        self.run_time = data['run_time']
        self.poster_pic = data['poster_pic']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_movie(cls, data):
        query = "INSERT INTO movies (title, description, trailer, rating, release_date, run_time, poster_pic user_id) VALUES ( %(title)s, %(description)s, %(trailer)s, %(rating)s, %(release_date)s, %(run_time)s, %(poster_pic)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
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
    

    # @classmethod
    # def get_users_for_proposal(cls, data):
    #     query = 'SELECT * FROM users LEFT JOIN proposals ON users.developer = proposals.skill1 AND users.language = proposals.skill2  WHERE proposals.id = %(proposal_id)s;'
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     users= []
    #     if results:
    #         for user in results:
    #             users.append(user)
    #         return users
    #     return users
    


    @staticmethod
    def validate_movie(data):
        is_valid = True
        if len(data['title'])<2:
            flash('Title must be more than 2 characters', 'movieTitle')
            is_valid = False
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'movieDescription')
            is_valid = False
        if data['rating']< 0 or data['rating'] > 5:
            flash('Our rating system supports 1-5 rating', 'movieRating')
            is_valid = False
        if not data['release_date']:
            flash('Please do not leave this blank', 'movieReleaseDate')
            is_valid = False
        if not data['run_time']:
            flash('Please do not leave this blank', 'movieRunTime')
            is_valid = False
        if not data['poster_pic']:
            flash('Please put a picture', 'moviePicture')
            is_valid = False
        else:
            flash('Movie successfully posted!', 'movieSuccess')
        return is_valid