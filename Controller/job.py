from flask import request, flash, redirect, url_for, render_template, Blueprint, abort
from sqlalchemy.exc import NoResultFound

from Model.models import Job, Resume
from app import db, app
from werkzeug.utils import secure_filename
import os  # Добавляем импорт для работы с файлами

from flask_login import login_required, current_user


import uuid

from forms import ApplyJobForm

UPLOAD_FOLDER = 'static/img/job_uploads'
app.config['UPLOAD_FOLDER'] = 'static/img/job_uploads'


job = Blueprint('job', __name__)


def init_job_blueprint(app):
    app.register_blueprint(job)


@job.route('/job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def show_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    apply_form = ApplyJobForm()
    apply_form.resumes.choices = [(r.id, r.title) for r in current_user.resumes if r.status]

    if apply_form.validate_on_submit():
        selected_resumes_ids = apply_form.resumes.data

        # Проверяем, не прикреплено ли уже выбранное резюме к вакансии
        existing_resumes = [resume for resume in job.resumes if resume.id in selected_resumes_ids]

        if existing_resumes:
            flash('Резюме уже прикреплено к этой вакансии!', 'error')
        else:
            selected_resumes = Resume.query.filter(Resume.id.in_(selected_resumes_ids)).all()
            job.resumes.extend(selected_resumes)
            db.session.commit()
            flash('Резюме успешно прикреплены к вакансии!', 'success')

    # Получаем все резюме, связанные с текущей вакансией
    job_resumes = job.resumes

    return render_template('show_job.html', job=job, apply_form=apply_form, job_resumes=job_resumes)


# В вашем коде
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@job.route("/create_job", methods=['POST', 'GET'])
@login_required
def create_job():
    try:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            requirements = request.form['requirements']
            image_file = request.files['image_file']

            # Добавляем обработку загрузки файла
            if image_file and allowed_file(image_file.filename):
                # Генерируем уникальное имя файла с использованием uuid
                filename = str(uuid.uuid4()) + secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None

            # Получаем регион текущего пользователя

            # Создаем работу, устанавливая регион равным региону пользователя
            new_job = Job(title=title, description=description, requirements=requirements, image_filename=filename, user=current_user)

            db.session.add(new_job)
            db.session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('CZN.jobs'))
    except Exception as e:
        error_message = f'An error occurred while adding the job: {str(e)}'
        flash(error_message, 'error')
        print(f"Error in create_job view: {error_message}")

    return render_template("create_job.html")


def save_file(file):
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None


def delete_file(filename):
    if filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)


@job.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('CZN.jobs'))

    # Проверяем, создал ли текущий пользователь эту работу
    if job.user_id != current_user.id:
        flash('You are not authorized to edit this job', 'error')
        return redirect(url_for('CZN.jobs'))

    if request.method == 'POST':
        # Delete the old file before updating the job
        delete_file(job.image_filename)

        job.title = request.form['title']
        job.description = request.form['description']
        job.requirements = request.form['requirements']

        # Save the new file
        job.image_filename = save_file(request.files['image_file'])

        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('CZN.jobs'))
        except:
            flash('An error occurred while updating the job', 'error')

    return render_template('edit_job.html', job=job)


@job.route('/job/<int:job_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('CZN.jobs'))

    # Проверяем, создал ли текущий пользователь эту работу
    if job.user_id != current_user.id:
        flash('You are not authorized to delete this job', 'error')
        return redirect(url_for('CZN.jobs'))

    if request.method == 'POST':
        try:
            db.session.delete(job)
            db.session.commit()
            flash('Job deleted successfully!', 'success')
            return redirect(url_for('CZN.jobs'))
        except:
            flash('An error occurred while deleting the job', 'error')

    return render_template('delete_job.html', job=job)


@job.route('/job/<int:job_id>/review', methods=['GET'])
@login_required
def review_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('CZN.jobs'))

    # Проверяем, является ли текущий пользователь администратором
    if not current_user.is_admin:
        flash('You are not authorized to review this job', 'error')
        return redirect(url_for('CZN.jobs'))

    return render_template('review_job.html', job=job)


@job.route('/job/<int:job_id>/reject', methods=['POST'])
@login_required
def reject_job(job_id):
    if not current_user.is_admin:
        abort(403)  # Отказ в доступе, если пользователь не является администратором

    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    if request.method == 'POST':
        job.status = False
        db.session.commit()

        flash('Job rejected successfully!', 'success')

    return redirect(url_for('job.admin_jobs'))


@job.route('/job/<int:job_id>/admin_approve', methods=['POST'])
@login_required
def admin_approve_job(job_id):
    if not current_user.is_admin:
        abort(403)  # Отказ в доступе, если пользователь не является администратором

    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    if request.method == 'POST':
        job.status = True
        db.session.commit()

        flash('Job approved successfully!', 'success')

    return redirect(url_for('job.admin_jobs'))


@job.route('/admin/jobs', methods=['GET'])
@login_required
def admin_jobs():
    # Проверяем, является ли текущий пользователь администратором
    if not current_user.is_admin:
        abort(403)  # Возвращаем ошибку 403 Forbidden для неадминистраторов

    # Получаем все вакансии, находящиеся на рассмотрении
    pending_jobs = Job.query.filter_by(status=None).all()

    return render_template('admin_jobs.html', pending_jobs=pending_jobs)

