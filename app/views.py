from app import app, db, lm
from flask import render_template, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_user import current_user, login_required, roles_accepted
from app.forms import RenameForm
from flask_restful import Api, Resource

api = Api(app)

#The Home page
@app.route('/')
def home_page():
    return render_template('pages/home_page.html')

@app.route('/user')
@login_required
def user_page():
    return render_template('pages/user_page.html')

@app.route('/admin')
@roles_accepted('admin')
def admin_page():
    return render_template('pages/admin_page.html')

@app.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    form = RenameForm(request.form, current_user)

    #If post
    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)

        db.session.commit()

        return redirect(url_for('home_page'))
    return render_template('pages/user_profile_page.html', form=form)
