from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = 'client/static/uploads/'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from client.auth import auth
    from client.views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    import client.database
    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return client.database.User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        if not path.exists('client/' + DB_NAME):
            db.create_all()
            print('Created Database!')