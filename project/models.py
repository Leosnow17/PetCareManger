from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    """Данные о пользователе"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    discord = db.Column(db.String(1000))
    steam = db.Column(db.String(1000))
    items = db.relationship('Post', backref='user')


class Post(db.Model):
    """Данные о посте"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag = db.Column(db.String(50))
    responded_user = db.Column(db.String(100), nullable=True, default="Пока никому. Станьте первым!")


class Setup(db.Model):
    """Данные об компьютере"""

    id = db.Column(db.Integer, primary_key=True)
    GPU = db.Column(db.String(500), nullable=False)
    CPU = db.Column(db.String(500), nullable=False)
    ram = db.Column(db.String(500))


class Item(db.Model):
    """Данные о предмете из магазина"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min = db.Column(db.String(100))
    max = db.Column(db.String(100))
    tag = db.Column(db.String(50))
    min_href = db.Column(db.String(200), nullable=False)
    max_href = db.Column(db.String(200), nullable=False)


class Pc(db.Model):
    """Конфигурация ПК"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    GPU = db.Column(db.String(500), nullable=False)
    CPU = db.Column(db.String(500), nullable=False)
    ram = db.Column(db.String(500))


class Game(db.Model):
    """Игра"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shops = db.Column(db.String(1000), nullable=True)
    trade = db.Column(db.String(1000), nullable=True)
    guide = db.Column(db.String(1000), nullable=True)
