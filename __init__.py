import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY']= 'd81b7b258f16e27c96a451e4'

app.config['RECAPTCHA_PUBLIC_KEY']='6LenbpwbAAAAADketTMxDDHHe8boWcLozMomh-S1'
app.config['RECAPTCHA_PRIVATE_KEY']='6LenbpwbAAAAAMfssgph0MgD3DswnfFQzgE8o6Gi'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'



from flask_app import routes



from flask_app import relations
app.register_blueprint(relations.bp)

from flask_app import search
app.register_blueprint(search.bp)