from flask import request, flash, redirect, url_for, render_template, Blueprint, abort

from Model.models import Resume
from app import db, app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid


resume = Blueprint('resume', __name__)


@resume.route('/resume/<int:resume_id>/detail')
@login_required
def detail_resume(resume_id):
    try:
        resume = Resume.query.get(resume_id)

        if not resume:
            abort(404, description="Резюме не найдено")

        # Проверяем, является ли текущий пользователь работодателем
        is_employer = current_user.is_authenticated and current_user.employer_status

        return render_template('detail_resume.html', resume=resume, is_employer=is_employer)
    except Exception as e:
        print(f"An error occurred in detail_resume view: {str(e)}")
        raise



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume.route("/create_resume", methods=['POST', 'GET'])
@login_required
def create_resume():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills = request.form['skills']
        image_file = request.files['image_file']

        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(str(uuid.uuid4()) + '_' + image_file.filename)
            image_path = os.path.join(app.static_folder, 'img', 'resume_uploads', image_filename)
            image_file.save(image_path)
        else:
            image_filename = None

        # Устанавливаем значение status в False по умолчанию
        status = None

        new_resume = Resume(title=title, description=description, skills=skills, image_filename=image_filename, user=current_user, status=status)

        try:
            db.session.add(new_resume)
            db.session.commit()
            flash('Резюме успешно создано!', 'success')
            return redirect(url_for('CZN.resumes'))
        except:
            flash('Произошла ошибка при добавлении резюме!', 'error')

    return render_template("create_resume.html")


def save_resume_image(image_file):
    if image_file and allowed_file(image_file.filename):
        # Генерируйте уникальное имя для файла, чтобы избежать конфликтов
        image_filename = secure_filename(str(uuid.uuid4()) + '_' + image_file.filename)
        image_path = os.path.join(app.static_folder, 'img', 'resume_uploads', image_filename)
        image_file.save(image_path)

        return image_filename
    return None
@resume.route('/resume/<int:resume_id>/edit', methods=['GET', 'POST'])
def edit_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    if request.method == 'POST':
        resume.title = request.form['title']
        resume.description = request.form['description']
        resume.skills = request.form['skills']

        # Получение файла из запроса
        new_image_file = request.files['new_image_file'] if 'new_image_file' in request.files else None

        # Удаление старого файла изображения и сохранение нового
        if new_image_file:
            delete_resume_image(resume.image_filename)
            resume.image_filename = save_resume_image(new_image_file)

        try:
            db.session.commit()
            flash('Resume updated successfully!', 'success')
            return redirect(url_for('CZN.resumes'))
        except:
            flash('An error occurred while updating the resume', 'error')

    return render_template('edit_resume.html', resume=resume)

@resume.route('/resume/<int:resume_id>/admin_approve', methods=['POST'])
@login_required
def admin_approve_resume(resume_id):
    if not current_user.is_admin:
        abort(403)  # Отказ в доступе, если пользователь не является администратором

    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    if request.method == 'POST':
        approve_value = request.form.get('approve')  # 'true' или 'false'

        if approve_value == 'true':
            resume.status = True
            flash('Resume approved successfully!', 'success')
        elif approve_value == 'false':
            resume.status = False
            flash('Resume rejected successfully!', 'success')

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('An error occurred while approving/rejecting the resume', 'error')

    return redirect(url_for('CZN.resumes'))


from Model.models import job_resume_association


@resume.route('/resume/<int:resume_id>/delete', methods=['GET', 'POST'])
def delete_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    if request.method == 'POST':
        try:
            # Удаляем связи резюме с вакансиями в таблице job_resume_association
            db.session.query(job_resume_association).filter_by(resume_id=resume_id).delete()

            # Затем удаляем само резюме
            db.session.delete(resume)
            db.session.commit()

            # Если всё прошло успешно, возвращаемся к списку резюме
            flash('Резюме успешно удалено!', 'success')
            return redirect(url_for('CZN.resumes'))
        except:
            # Если произошла ошибка, откатываем изменения и выводим сообщение об ошибке
            db.session.rollback()
            flash('Произошла ошибка при удалении резюме!', 'error')

    return render_template('delete_resume.html', resume=resume)



def delete_resume_image(image_filename):
    if image_filename:
        image_path = os.path.join(app.static_folder, 'img', 'resume_uploads', image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

@resume.route('/admin/pending_resumes')
@login_required
def admin_pending_resumes():
    if not current_user.is_admin:
        abort(403)  # Отказ в доступе, если пользователь не является администратором

    pending_resumes = Resume.query.filter_by(status=None).all()

    return render_template('admin_pending_resumes.html', resumes=pending_resumes)


