from flask import request, flash, redirect, url_for, render_template, Blueprint, abort

from Model.models import Resume
from app import db

resume = Blueprint('resume', __name__)

@resume.route('/resume/<int:resume_id>/detail')
def detail_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    return render_template('detail_resume.html', resume=resume)

@resume.route("/create_resume", methods=['POST', 'GET'])
def create_resume():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills = request.form['skills']

        new_resume = Resume(title=title, description=description, skills=skills)

        try:
            db.session.add(new_resume)
            db.session.commit()
            flash('Resume created successfully!', 'success')
            return redirect(url_for('resumes'))
        except:
            flash('An error occurred while adding the resume!', 'error')

    return render_template("create_resume.html")


@resume.route('/resume/<int:resume_id>/edit', methods=['GET', 'POST'])
def edit_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    if request.method == 'POST':
        resume.title = request.form['title']
        resume.description = request.form['description']
        resume.skills = request.form['skills']

        try:
            db.session.commit()
            flash('Resume updated successfully!', 'success')
            return redirect(url_for('resumes'))
        except:
            flash('An error occurred while updating the resume', 'error')

    return render_template('edit_resume.html', resume=resume)



@resume.route('/resume/<int:resume_id>/delete', methods=['GET', 'POST'])
def delete_resume(resume_id):
    resume = Resume.query.get(resume_id)

    if not resume:
        abort(404, description="Резюме не найдено")

    if request.method == 'POST':
        try:
            db.session.delete(resume)
            db.session.commit()
            flash('Resume deleted successfully!', 'success')
            return redirect(url_for('resumes'))
        except:
            flash('An error occurred while deleting the resume', 'error')

    return render_template('delete_resume.html', resume=resume)
