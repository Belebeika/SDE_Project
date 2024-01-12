from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from Model.models import User, Job, Resume, Region
from forms import RegionForm

CZN = Blueprint('CZN', __name__)

@CZN.route('/')
def index():
    title = 'Главное меню'
    return render_template('index.html', title=title)
@CZN.route("/jobs", methods=['GET', 'POST'])
def jobs():
        # Проверяем, залогинен ли пользователь
        if current_user.is_authenticated:
            # Получаем объект региона текущего пользователя
            selected_region = Region.query.get(current_user.region_id)

            # Если пользователь залогинен, отображаем вакансии без формы
            jobs = Job.query.all()
            return render_template('jobs.html', jobs=reversed(jobs), selected_region=selected_region)

        # Если пользователь анонимный, отображаем форму выбора региона
        form = RegionForm()
        if form.validate_on_submit():
            region_choices = [(region.id, region.name) for region in Region.query.all()]
            selected_region_id = form.region.data
            jobs_in_region = Job.query.filter_by(region_id=selected_region_id).all()
            return render_template('region_selection.html', form=form, region_choices=region_choices)

        return render_template('region_selection.html', form=form)




@CZN.route("/resumes")
@login_required
def resumes():
    resumes = Resume.query.filter_by(user=current_user).all()
    return render_template('resumes.html', resumes=reversed(resumes))
