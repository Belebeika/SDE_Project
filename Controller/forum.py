#forum.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import *

from app import db
from Model.models import User

forum = Blueprint('forum', __name__)

@forum.route('/')
def index():
    title = 'Главное меню'
    return render_template('index.html', title=title)

@forum.route('/vacancy')
def vacancy():
    title = 'Главное меню'
    return render_template('vacancy.html', title=title)

@forum.route('/rezume')
def rezume():
    title = 'Главное меню'
    return render_template('rezume.html', title=title)

