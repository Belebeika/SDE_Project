from flask import request, flash, redirect, url_for, render_template, Blueprint, abort
from Model.models import Job
from app import db

job = Blueprint('job', __name__)

def init_job_blueprint(app):
    app.register_blueprint(job)



@job.route('/job/<int:job_id>')
def show_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    return render_template('show_job.html', job=job)

@job.route("/create_job", methods=['POST', 'GET'])

def create_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']

        new_job = Job(title=title, description=description, requirements=requirements)

        try:
            db.session.add(new_job)
            db.session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('jobs'))
        except:
            flash('An error occurred while adding the job!', 'error')

    return render_template("create_job.html")

@job.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        job.requirements = request.form['requirements']

        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs'))
        except:
            flash('An error occurred while updating the job', 'error')

    return render_template('edit_job.html', job=job)



@job.route('/job/<int:job_id>/delete', methods=['GET', 'POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        abort(404, description="Вакансия не найдена")

    if request.method == 'POST':
        try:
            db.session.delete(job)
            db.session.commit()
            flash('Job deleted successfully!', 'success')
            return redirect(url_for('jobs'))
        except:
            flash('An error occurred while deleting the job', 'error')

    return render_template('delete_job.html', job=job)
