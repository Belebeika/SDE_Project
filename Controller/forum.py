#forum.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import *

from Model.models import User, Job, Resume

forum = Blueprint('forum', __name__)


@forum.route('/')
def index():
    title = 'Главное меню'
    return render_template('index.html', title=title)


@forum.route("/jobs")
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=reversed(jobs))


@forum.route("/resumes")
def resumes():
    resumes = Resume.query.all()
    return render_template('resumes.html', resumes=reversed(resumes))

