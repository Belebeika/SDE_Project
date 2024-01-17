#forms.py
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, StringField, SubmitField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import EqualTo, Email, DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from Model.models import Region


class RegistrationForm(FlaskForm):
    firstname = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Фамилия пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    age = StringField('Возраст', validators=[DataRequired(), Length(min=1, max=3)])
    region = SelectField('Регион', coerce=int, validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    employer_status = BooleanField('Статус работодателя')
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegionForm(FlaskForm):
    region = SelectField('Регион', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Показать вакансии')


class ApplyJobForm(FlaskForm):
    resumes = SelectMultipleField('Выбрать резюме', coerce=int)
    submit = SubmitField('Прикрепить')

