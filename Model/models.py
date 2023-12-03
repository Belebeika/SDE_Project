# models.py
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128))  # Изменить поле пароля на хэш пароля
    email = db.Column(db.String(80), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # Хэширование пароля

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # На странице со всеми вакансиями
    title = db.Column(db.String, nullable=False)
    # На странице вакансии
    text = db.Column(db.String, nullable=False)
    # Изображение вакансии на вкладке с прокруткой вакансий
    title_image = db.Column(db.LargeBinary, nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('forum_posts', lazy=True))
    pass

# Изображения отображаемые на странице с вакансией
class Vacancy_images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    Vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'), nullable=False)
    vacancy = db.relationship('Vacancy', backref=db.backref('forum_posts', lazy=True))
    pass

class Rezume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # На странице со всеми резюме
    title = db.Column(db.String, nullable=False)
    # На странице резюме
    text = db.Column(db.String, nullable=False)
    # Изображение резюме на вкладке с прокруткой резюме
    title_image = db.Column(db.LargeBinary, nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rezumes', lazy=True))
    pass

# Изображения отображаемые на странице с резюме
class Rezume_images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    Rezume_id = db.Column(db.Integer, db.ForeignKey('rezume.id'), nullable=False)
    rezume = db.relationship('Rezume', backref=db.backref('rezume_images', lazy=True))
    pass