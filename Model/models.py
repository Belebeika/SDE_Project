from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    employer_status = db.Column(db.Boolean, nullable=False)
    workplace = db.Column(db.String(20))  # место работы
    post = db.Column(db.String(20))  # должность
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', backref=db.backref('users', lazy=True))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)



class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(200))
    image_filename = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('resumes', lazy=True))
    status = db.Column(db.Boolean, nullable=True)


job_resume_association = db.Table(
    'job_resume_association',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('resume_id', db.Integer, db.ForeignKey('resume.id'))
)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.String(200))
    image_filename = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('jobs', lazy=True))
    status = db.Column(db.Boolean, nullable=True)
    resumes = db.relationship('Resume', secondary=job_resume_association, backref=db.backref('jobs', lazy=True))






