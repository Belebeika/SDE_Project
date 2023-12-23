from flask import request, flash, Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from forms import EditProfileForm

profile = Blueprint('profile', __name__)


@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.region = form.region.data
        current_user.age = form.age.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('forum.profile'))

    return render_template('edit_profile.html', form=form)
