from flask_app import app
from flask import render_template, redirect, url_for, flash
from flask import request
from flask_app import db
from flask_login import login_user, logout_user, login_required

from flask_app.models import User, Child, Parent
from flask_app.forms import RegisterForm, LoginForm, ChildSearchForm
from flask_app import search


@app.context_processor
def inject_template_globals():
    categories =Parent.query.all()
    return dict(categories=categories) 

@app.route("/",  methods=('GET', 'POST'))
def home():
    childs =Child.query.all()

    form = ChildSearchForm(request.form)
    form.parent.choices = [(g.id, g.name) for g in Parent.query.order_by('id')]
    if request.method == 'POST':
        return search.search_results(form)
        #return redirect(url_for('search.search_results'))
    return render_template('home.html', childs=childs, form=form)

@app.route('/users')
@login_required
def users_page():
	users = User.query.all()
	return render_template('users.html', users=users)

@app.route('/colors')
def colors_page():
    return render_template('colors.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully. You are now loggin as {user_to_create.name}', category='success')

        return redirect(url_for('home'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.name.data).first()
        
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):  
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash('You have been logged out', category = 'info')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404


