import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
#from itsdangerous.url_safe import URLSafeSerializer
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sitemap import Sitemap

app = Flask(__name__)
ext = Sitemap(app=app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

app.config['SECRET_KEY']= ''

app.config['RECAPTCHA_PUBLIC_KEY']='-'
app.config['RECAPTCHA_PRIVATE_KEY']=''

#app.config.from_pyfile('config.cfg')

app.config['MAIL_SERVER']=''
app.config['MAIL_PORT'] = 
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
allurls = ext._generate_all_urls()


from flask_app import routes

from flask_app import relations
app.register_blueprint(relations.bp)

from flask_app import search
app.register_blueprint(search.bp)

from flask_app import cart
app.register_blueprint(cart.bp)

from flask_app import geomap
app.register_blueprint(geomap.bp)
