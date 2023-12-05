from flask import Blueprint, render_template, redirect, url_for, request

from flask import render_template, redirect, url_for
from flask_login import current_user, login_required


from Model.models import Vacancy
from Model.models import Rezume




from wtforms.validators import EqualTo, Email, DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed



vacancyAndResume = Blueprint('vacancyAndResume', __name__)

from app import db



class VacancyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    title_image = FileField('Title Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')



class ResumeForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Submit')

@vacancyAndResume.route('/vacancies')
def vacancies():
    vacancies = Vacancy.query.all()
    return render_template('vacancy.html', vacancies=vacancies)

@vacancyAndResume.route('/resumes')
def resumes():
    resumes = Rezume.query.all()
    return render_template('resume.html', resumes=resumes)@vacancyAndResume.route('/add_vacancy', methods=['GET', 'POST'])
@vacancyAndResume.route('/add_vacancy', methods=['GET', 'POST'])
@login_required
def add_vacancy():
    form = VacancyForm()
    if form.validate_on_submit():
        new_vacancy = Vacancy(
            title=form.title.data,
            text=form.text.data,
            user= current_user # Предполагая, что у вас есть текущий пользователь (возможно, используется Flask-Login)
        )
        if form.title_image.data:  # Проверка наличия загруженного файла
            new_vacancy.title_image = form.title_image.data.read()
        db.session.add(new_vacancy)
        db.session.commit()
        return redirect(url_for('vacancyAndResume.vacancies'))
    return render_template('add_vacancy.html', form=form)


@vacancyAndResume.route('/edit_vacancy/<int:vacancy_id>', methods=['GET', 'POST'])
def edit_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    form = VacancyForm()
    if form.validate_on_submit():
        vacancy.title = form.title.data
        vacancy.text = form.text.data
        if form.title_image.data:
            vacancy.title_image = form.title_image.data.read()
        db.session.commit()
        return redirect(url_for('vacancyAndResume.vacancies'))
    elif request.method == 'GET':
        form.title.data = vacancy.title
        form.text.data = vacancy.text
    return render_template('edit_vacancy.html', form=form, vacancy=vacancy)

@vacancyAndResume.route('/delete_vacancy/<int:vacancy_id>')
def delete_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    db.session.delete(vacancy)
    db.session.commit()
    return redirect(url_for('vacancyAndResume.vacancies'))

@vacancyAndResume.route('/add_resume', methods=['GET', 'POST'])
def add_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        new_resume = Rezume(title=form.title.data)
        db.session.add(new_resume)
        db.session.commit()
        return redirect(url_for('vacancyAndResume.resumes'))
    return render_template('add_resume.html', form=form)

@vacancyAndResume.route('/edit_resume/<int:resume_id>', methods=['GET', 'POST'])
def edit_resume(resume_id):
    resume = Rezume.query.get_or_404(resume_id)
    form = ResumeForm()
    if form.validate_on_submit():
        resume.title = form.title.data
        db.session.commit()
        return redirect(url_for('vacancyAndResume.resumes'))
    elif request.method == 'GET':
        form.title.data = resume.title
    return render_template('edit_resume.html', form=form)

@vacancyAndResume.route('/delete_resume/<int:resume_id>')
def delete_resume(resume_id):
    resume = Rezume.query.get_or_404(resume_id)
    db.session.delete(resume)
    db.session.commit()
    return redirect(url_for('vacancyAndResume.resumes'))
