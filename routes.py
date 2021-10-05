from flask_app import app, ext, allurls
from flask import render_template, redirect, url_for, flash, send_from_directory
from flask import request
from flask_app import db, s, mail
from flask_login import login_user, logout_user, login_required

from flask_app.models import User, Child, Parent
from flask_app.forms import RegisterForm, LoginForm, ChildSearchForm
from flask_app import search
from flask_mail import Mail, Message
from datetime import datetime

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
                              password=form.password1.data
                              )
        
        email = form.email_address.data
        name = form.name.data
        token = s.dumps(email,salt='email-confirm')

        msg = Message('Confirm Email', sender='emanuelapetri@gmail.com', recipients=[email])

        link = url_for('relations.confirm_email', token=token, _external=True)

        msg.body = 'Your link is {}'.format(link)

        #msg.body = render_template('template.txt', **kwargs)
        msg.html = render_template('mail_activate.html', link=link, name=name)

        mail.send(msg)
       
        db.session.add(user_to_create)
        db.session.commit()

        #login_user(user_to_create)
        #flash(f'Account created successfully. You are now loggin as {user_to_create.name}', category='success')
        flash(f'Please, see your mails to activate your account', category='success')
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.name.data).first()
        
        if attempted_user.email_confirmed==1:

            if attempted_user and attempted_user.check_password_correction(
                    attempted_password=form.password.data
            ):  
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.name}', category='success')
                return redirect(url_for('home'))
            else:
                flash('Username and password are not match! Please try again', category='danger')
        else:
            flash('You must validate your email', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash('You have been logged out', category = 'info')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404

@ext.register_generator
def index():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True

    yield 'home',{},
    yield 'geomap.geomap_page',{},
    yield 'relations.parents',{},
    
    childs=Child.query.all()
    for child in childs:
        if child.child_date_updated:
            date=child.child_date_updated
        else:
            date=child.child_date_created
        yield 'relations.child', {'name': child.name}, date, 'never', 0.7
    



    


