from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from Model.models import User, Job, Resume, Region
from forms import RegionForm

CZN = Blueprint('CZN', __name__)

@CZN.route('/')
def index():
    title = 'Главное меню'
    return render_template('index.html', title=title)
from flask import request
from flask import request

from flask import request

@CZN.route("/jobs", methods=['GET', 'POST'])
def jobs():
    # Получаем выбранный регион и статус из параметров запроса
    selected_region_id = request.args.get('region', 'all')
    status = request.args.get('status', 'all')

    # Получаем список всех регионов из базы данных
    regions = Region.query.all()

    selected_region = None
    # Если пользователь залогинен
    if current_user.is_authenticated:
        # Если пользователь - админ
        if current_user.is_admin:
            # Если выбран конкретный регион
            if selected_region_id != 'all':
                # Фильтруем вакансии по выбранному региону и статусу
                if status == 'pending':
                    jobs = Job.query.join(User).filter(User.region_id==selected_region_id, (Job.status==None) | (Job.user_id==current_user.id)).all()
                elif status == 'approved':
                    jobs = Job.query.join(User).filter(User.region_id==selected_region_id, (Job.status==True) | (Job.user_id==current_user.id)).all()
                elif status == 'rejected':
                    jobs = Job.query.join(User).filter(User.region_id==selected_region_id, (Job.status==False) | (Job.user_id==current_user.id)).all()
                else:
                    jobs = Job.query.join(User).filter(User.region_id==selected_region_id, (Job.user_id==current_user.id)).all()
            # Если выбраны все регионы
            else:
                if status == 'pending':
                    jobs = Job.query.join(User).filter((Job.status==None) | (Job.user_id==current_user.id)).all()
                elif status == 'approved':
                    jobs = Job.query.join(User).filter((Job.status==True) | (Job.user_id==current_user.id)).all()
                elif status == 'rejected':
                    jobs = Job.query.join(User).filter((Job.status==False) | (Job.user_id==current_user.id)).all()
                else:
                    jobs = Job.query.join(User).filter((Job.user_id==current_user.id)).all()
        # Если пользователь не админ
        else:
            # Фильтруем вакансии, показывая только одобренные и те, которые создал текущий пользователь
            jobs = Job.query.filter((Job.status==True) | (Job.user_id==current_user.id)).all()

        # Получаем объект региона текущего пользователя
        selected_region = Region.query.get(current_user.region_id)

    # Если пользователь не авторизован
    else:
        if selected_region_id != 'all':
            # Фильтруем вакансии по выбранному региону
            jobs = Job.query.join(User).filter(User.region_id==selected_region_id, Job.status==True).all()
        else:
            # Показываем только одобренные вакансии
            jobs = Job.query.filter_by(status=True).all()

    return render_template('jobs.html', jobs=reversed(jobs), selected_region=selected_region, regions=regions)




@CZN.route("/resumes", methods=['GET', 'POST'])
@login_required
def resumes():
    if current_user.is_admin:
        # Получаем выбранный статус из параметров запроса
        status = request.args.get('status', 'all')

        # Фильтруем резюме по статусу
        if status == 'pending':
            resumes = Resume.query.filter_by(status=None).all()
        elif status == 'approved':
            resumes = Resume.query.filter_by(status=True).all()
        elif status == 'rejected':
            resumes = Resume.query.filter_by(status=False).all()
        else:
            resumes = Resume.query.all()

        return render_template('resumes.html', resumes=reversed(resumes), is_admin=current_user.is_admin)

    # Если пользователь не является администратором, оставляем текущую логику
    resumes = Resume.query.filter_by(user=current_user).all()
    return render_template('resumes.html', resumes=reversed(resumes), is_admin=current_user.is_admin)


@CZN.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
