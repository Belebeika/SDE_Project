from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from Model.models import User
from app import db
from forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)
from flask import render_template
from Model.models import Region

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    form.region.choices = [(region.id, region.region) for region in Region.query.all()]

    try:
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            age = form.age.data
            region_id = form.region.data
            email = form.email.data
            phone_number = form.phone_number.data
            employer_status = form.employer_status.data


            userdb = User.query.filter_by(email=email).first()

            if userdb is not None and userdb.email == email:
                flash("Пользователь с таким email уже существует")
                return redirect(url_for('auth.register'))

            user = User(firstname=firstname, lastname=lastname, age=age, region_id=region_id, email=email,
                        phone_number=phone_number, employer_status=employer_status)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('CZN.index'))
    except Exception as e:
        print(f"An error occurred in register view: {str(e)}")
        raise

    print(form.errors)
    return render_template('register.html', form=form)




@auth.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not User.verify_password(user,password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('CZN.index'))

    return render_template('login.html', form=form)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('CZN.index'))
