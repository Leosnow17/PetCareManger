from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

UPLOAD_FOLDER_PETS = r'/Users/grigorijsvalev/PycharmProjects/game_agregator/project/static/images/pets'
UPLOAD_FOLDER_VETS = r'/Users/grigorijsvalev/PycharmProjects/game_agregator/project/static/images/vets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# /home/gameaggergator/game_agregator/project/static/images/pets
# /home/gameaggergator/game_agregator/project/static/images/vets

def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER_PETS'] = UPLOAD_FOLDER_PETS
    app.config['UPLOAD_FOLDER_VETS'] = UPLOAD_FOLDER_VETS

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app