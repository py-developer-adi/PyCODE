'''coderadi'''

# ? Importing Libraries
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# ! Constants
db = SQLAlchemy()
logger = LoginManager()

# ? User Database Model
class User(db.Model, UserMixin): #! Incomplete (Client/Admin)
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    is_beta = db.Column(db.Boolean, default=False)
    
    @property
    def is_authenticated(self):
        return True
    
    def get_id(self):
        return self.username
    
# ? Product Model Database Model
class Model(db.Model): #: Complete (Admin)
    __tablename__ = 'model'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String, primary_key=True)
    model = db.Column(db.String, unique=True)
    series = db.Column(db.String)
    price = db.Column(db.Float)
    desc = db.Column(db.String)
    overview = db.Column(db.String)
    preview = db.Column(db.String)
    cover = db.Column(db.String)
    limit = db.Column(db.String)
    is_featured = db.Column(db.Boolean, default=False)
    
# ? Article Database Model
class Article(db.Model): #: Complete (Admin)
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    cover = db.Column(db.String)
    is_featured = db.Column(db.Boolean, default=False)
    url = db.Column(db.String)
    
# ? Voucher Database Model
class Voucher(db.Model): #: Complete (Admin)
    __tablename__ = 'voucher'
    __table_args__ = {'extend_existing': True}
    code = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    discount = db.Column(db.Float)
    limit = db.Column(db.Integer)
    expiry = db.Column(db.String)
    
# ? Feedback
class Feed(db.Model): #! Incomplete (Client)
    __tablename__ = 'feed'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    feedback = db.Column(db.String)
    
# ? Service Database Model
class Service(db.Model): #: Complete (Admin)
    __tablename__ = 'service'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    cover = db.Column(db.String)
    desc = db.Column(db.String)
    is_featured = db.Column(db.Boolean, default=False)
    info = db.Column(db.String)
    
# ? Contact Database Model
class Contact(db.Model): #! Incomplete (Client)
    __tablename__ = 'contact'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    topic = db.Column(db.String)
    desc = db.Column(db.String)