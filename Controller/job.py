from flask import request, flash, redirect, url_for, render_template, Blueprint, abort
from Model.models import Job
from app import db, app
from werkzeug.utils import secure_filename
import os  # Добавляем импорт для работы с файлами

from flask_login import login_required, current_user


import uuid

UPLOAD_FOLDER = 'static/img/job_uploads'
app.config['UPLOAD_FOLDER'] = 'static/img/job_uploads'



job = Blueprint('job', __name__)

def init_job_blueprint(app):
    app.register_blueprint(job)



@job.route('/job/<int:job_id>')
def show_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    return render_template('show_job.html', job=job)

# В вашем коде
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@job.route("/create_job", methods=['POST', 'GET'])
@login_required
def create_job():
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
        user_region = current_user.region

        # Создаем работу, устанавливая регион равным региону пользователя
        new_job = Job(title=title, description=description, requirements=requirements, image_filename=filename, author=current_user, region=user_region)

        try:
            db.session.add(new_job)
            db.session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('CZN.jobs'))
        except:
            flash('An error occurred while adding the job!', 'error')

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
    if job.author != current_user:
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
    if job.author != current_user:
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

