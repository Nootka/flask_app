from datetime import datetime
from flask_app import db, login_manager
from flask_app import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	location = db.Column(db.String(50))
	date_created = db.Column(db.DateTime,default=datetime.now)
	password_hash = db.Column(db.String(60), nullable=False)
	email_address = db.Column(db.String(50), nullable=False, unique=True)
	email_confirmed = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		return self.password

	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
			

	def check_password_correction(self, attempted_password):
		return bcrypt.check_password_hash(self.password_hash, attempted_password)
		#if check_password_hash(user.pw_hashed, form.password.data):

	#def __repr__(self):
		#return '<User %r>' % self.name

class Parent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500))
	child=db.relationship('Child', backref='parent')

	def __repr__(self):
		return f'Parent {self.name}'

class Unit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500))
	child=db.relationship('Child', backref='unit')

class PlaceCoordinates(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	latitude=db.Column(db.String(500))
	longitude=db.Column(db.String(500))
	child=db.relationship('Child', backref='place_coordinates')

	def __repr__(self):
		return f'Item {self.name}'
		
class Child(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500))
	parent_id=db.Column(db.Integer(), db.ForeignKey('parent.id'))
	unit_id=db.Column(db.Integer(), db.ForeignKey('unit.id'))
	placecoordinates_id=db.Column(db.Integer(), db.ForeignKey('place_coordinates.id'))
	image_url= db.Column(db.String(500))
	description=description = db.Column(db.Text)
	child_date_created = db.Column(db.DateTime,default=datetime.now)
	child_date_updated = db.Column(db.DateTime)
	
	def __repr__(self):
		return f'Item {self.name}'



