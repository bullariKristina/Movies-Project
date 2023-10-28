from flask_app import app

from flask_app.controllers import movies, users, genres, env 

if __name__=='__main__':
    app.run(debug=True)
