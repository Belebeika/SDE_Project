from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from Model.models import User, Job, Resume
from forms import RegionForm

forum = Blueprint('forum', __name__)


@forum.route('/profile')
@login_required  # Декоратор, чтобы требовать аутентификации пользователя
def profile():
    return render_template('profile.html', user=current_user)


@forum.route('/')
def index():
    title = 'Главное меню'
    return render_template('index.html', title=title)


@forum.route("/jobs", methods=['GET', 'POST'])
def jobs():
    # Проверяем, залогинен ли пользователь
    if current_user.is_authenticated:
        # Если пользователь залогинен, отображаем вакансии без формы
        jobs = Job.query.all()
        return render_template('jobs.html', jobs=reversed(jobs))

    # Если пользователь анонимный, отображаем форму выбора региона
    form = RegionForm()

    if form.validate_on_submit():
        region = form.region.data
        jobs_in_region = Job.query.filter_by(region=region).all()
        return render_template('jobs.html', jobs=reversed(jobs_in_region), form=form)

    return render_template('region_selection.html', form=form)


@forum.route("/resumes")
@login_required
def resumes():
    resumes = Resume.query.filter_by(user=current_user).all()
    return render_template('resumes.html', resumes=reversed(resumes))
