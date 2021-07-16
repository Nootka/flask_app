from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_app.models import User
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class RegisterForm(FlaskForm):
	def validate_username(self, username_to_check):
		user = User.query.filter_by(name=username_to_check.data).first()
		if user:
			raise ValidationError('Username already exists! Please try a different username')

	def validate_email_address(self, email_address_to_check):
		email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
		if email_address:
			raise ValidationError('Email Address already exists! Please try a different email address')
	
	name = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
	email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
	password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
	password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
	submit = SubmitField(label='Create Account')
	recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
	name = StringField(label='User Name:', validators=[DataRequired()])
	password = PasswordField(label='Password:', validators=[DataRequired()])
	submit = SubmitField(label='Sign in')


class ParentForm(FlaskForm):
	name = StringField(label='parent Name', validators=[DataRequired()])
	submit = SubmitField(label='Create')

class UnitForm(FlaskForm):
	name = StringField(label='Unit Name', validators=[DataRequired()])
	submit = SubmitField(label='Create')

class ChildForm(FlaskForm):
	name = StringField(label='Name', validators=[DataRequired()])
	image =FileField(label='Image')
	parent =SelectField(u'Group', coerce=int)
	unit =SelectField(u'Unit', coerce=int)
	description = TextAreaField(label='Description')
	price = IntegerField(label='Price')
	submit = SubmitField(label='Create')

class ChildSearchForm(FlaskForm):
	parent = SelectField(u'Group', coerce=int)
	search = StringField(label='Name')
	submit = SubmitField(label='Search')
