from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

UPLOAD_FOLDER = 'server/static/uploads/'
OUTPUT_FOLDER = 'server/static/transferImages/'

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://khanh:230604@192.168.1.52/FLASK_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from server.auth import auth
    from server.views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    import server.database

    @login_manager.user_loader
    def load_user(id):
        return server.database.User.query.get(int(id))

    return app


