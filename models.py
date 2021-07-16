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

	#products = db.relationship('Product', backref='owned_user', lazy=True)

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

class Costumer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(500),nullable=False)
	city = db.Column(db.String(50),nullable=False)
	postcode = db.Column(db.String(50),nullable=False)
	email = db.Column(db.String(50),nullable=False, unique= True)
	orders = db.relationship('Order', backref='costumer', lazy=True)

#crear una tabla en la bd sin clase
# porque la relacion entre product y order es mas compleja: many-to-many
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('child.id'), primary_key=True)
    )

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	shipped_date = db.Column(db.DateTime)
	delivered_date = db.Column(db.DateTime)
	coupon = db.Column(db.String(50))
	costumer_id = db.Column(db.Integer, db.ForeignKey('costumer.id'), nullable=False)

	products = db.relationship('Child', secondary='order_product')


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

		
class Child(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(500))
	parent_id=db.Column(db.Integer(), db.ForeignKey('parent.id'))
	unit_id=db.Column(db.Integer(), db.ForeignKey('unit.id'))
	image_url= db.Column(db.String(500))
	description=description = db.Column(db.Text)
	price=db.Column(db.Integer)

	def __repr__(self):
		return f'Item {self.name}'

