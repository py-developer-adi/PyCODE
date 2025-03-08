'''coderadi'''

# ? Importing Libraries
from flask import Flask, Blueprint, render_template, request, redirect, flash
from models import *
from uuid import uuid4
import os, shutil

# ! Folder Constants
static_store = "static/store"
static_article = "static/articles"
temp_store = "templates/store"
temp_article = "templates/articles"
static_service = "static/service"
temp_service = "templates/service"

os.makedirs(static_store, exist_ok=True)
os.makedirs(temp_store, exist_ok=True)
os.makedirs(temp_article, exist_ok=True)
os.makedirs(static_article, exist_ok=True)
os.makedirs(static_service, exist_ok=True)
os.makedirs(temp_service, exist_ok=True)

# ! Server Configurations
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pycode.sqlite3'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SECRET_KEY'] = 'py-code.in'

# ! Models Initializations
db.init_app(server)
logger.init_app(server)
migrate = Migrate(server, db)

# | Admin Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

# * User Loader
@logger.user_loader
def load_user(user):
    return db.session.get(User, user)

@server.before_request
def load_admin():
    if User.query.filter_by(username='coderadi').first() is None:
        new_user = User(username='coderadi', email='adiprofitcoder@gmail.com', 
                        password=generate_password_hash('Aditya@458'), is_admin=True)
        db.session.add(new_user)
        db.session.commit()
    
@admin.before_request
def check_admin():
    if not current_user.is_admin:
        flash("Invalid user URL", "error")
        return redirect('/home')

# ? Admin Routes
@admin.route('/')
def log():
    if current_user.is_admin:
        return redirect('/admin/dash')
    return redirect('/login')

@admin.route('/dash')
def dash():
    models = Model.query.all()
    articles = Article.query.all()
    services = Service.query.all()
    feeds = Contact.query.all()
    users = User.query.all()
    return render_template(
        'admin/dash.html', models=models, articles=articles, services=services,
        feeds=feeds, users=users
    )

@admin.route('/add-model', methods=['GET', 'POST'])
def add_model():
    if request.method == 'GET':
        return render_template('admin/add_model.html')
    else:
        id = request.form.get('model-id')
        model = request.form.get('model')
        series = request.form.get('series')
        price = request.form.get('price')
        desc = request.form.get('desc')
        overview = request.files.get('overview')
        preview = request.files.get('preview')
        cover = request.files.get('cover')
        assets = request.files.getlist('assets')
        limit = request.form.get('limit')        
        is_featured = True if request.form.get('is_featured') == 'on' else False
        
        model_temp_folder = os.path.join(temp_store, id)
        model_static_folder = os.path.join(static_store, id)
        os.mkdir(model_temp_folder)
        os.mkdir(model_static_folder)
        
        overview_url = f"store/{id}/{overview.filename}"
        preview_url = f"store/{id}/{preview.filename}"
        cover_url = f"store/{id}/{cover.filename}"
        
        overview.save(f"{model_temp_folder}/{overview.filename}")
        preview.save(f"{model_static_folder}/{preview.filename}")
        cover.save(f"{model_static_folder}/{cover.filename}")
        
        for elem in assets:
            print(f"{model_static_folder}/{elem.filename}")
            elem.save(f"{model_static_folder}/{elem.filename}")
        
        new_model = Model(
            id=id,
            model=model, series=series, price=price, desc=desc, overview=overview_url, preview=preview_url,
            cover=cover_url, limit=limit, is_featured=is_featured
        )
        db.session.add(new_model)
        db.session.commit()
        flash(f"Model {model} successfully added!", "success")
        return redirect('/admin/dash')
        

@admin.route('/add-article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        return render_template('admin/add_article.html') 
    else:
        id = request.form.get('article-id')
        title = request.form.get('title')
        is_featured = True if request.form.get('is_featured') == 'on' else False
        cover = request.files.get('cover')
        url = request.files.get('url')
        assets = request.files.getlist('assets')
        
        temp_article_file = os.path.join(temp_article, id)
        static_article_file = os.path.join(static_article, id)
        os.mkdir(temp_article_file)
        os.mkdir(static_article_file)
        
        cover_url = f'articles/{id}/{cover.filename}'
        url_url = f'articles/{id}/{url.filename}'
        
        cover.save(os.path.join(static_article_file, cover.filename))
        url.save(os.path.join(temp_article_file, url.filename))
        
        for asset in assets:
            asset.save(os.path.join(static_article_file, f'{asset.filename}'))
        
        new_article = Article(
            id=id, title=title, cover=cover_url, is_featured=is_featured, url=url_url
        )
        db.session.add(new_article)
        db.session.commit()
        
        flash(f"New Article {title} added", "success")
        return redirect('/admin/dash')
    
@admin.route('/update-article/<article_id>', methods=['GET', 'POST'])
def update_article(article_id):
    if request.method == 'GET':
        article = Article.query.filter_by(id=article_id).first()
        return render_template('admin/update_article.html', article=article)
    else:
        article = Article.query.filter_by(id=article_id).first()
        assets = request.files.getlist('assets')
        
        static_article_file = os.path.join(static_article, article.id)
        
        for asset in assets:
            asset.save(os.path.join(static_article_file, f'{asset.filename}'))
            
        flash(f"Article {article.title} upgraded", "success")
        return redirect('/admin/dash')
        

@admin.route('/add-service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'GET':
        return render_template('admin/add_service.html')
    else:
        id = request.form.get('service-id')
        title = request.form.get('title')
        desc = request.form.get('desc')
        cover = request.files.get('cover')
        is_featured = True if request.form.get('is_featured') == 'on' else False
        info = request.files.get('info')
        assets = request.files.getlist('assets')
        
        static_service_folder = os.path.join(static_service, id)
        temp_service_folder = os.path.join(temp_service, id)
        os.mkdir(static_service_folder)
        os.mkdir(temp_service_folder)
        
        cover_url = f"service/{id}/{cover.filename}"
        info_url = f"service/{id}/{info.filename}"
        cover.save(os.path.join(static_service_folder, cover.filename))
        info.save(os.path.join(temp_service_folder, info.filename))
        
        for asset in assets:
            asset.save(f"{static_service_folder}/{asset.filename}")
        
        new_service = Service(
            id=id, title=title, desc=desc, cover=cover_url, info=info_url, is_featured=is_featured
        )
        db.session.add(new_service)
        db.session.commit()
        
        flash(f"New Service {title} added", "success")
        return redirect('/admin/dash')

@admin.route('/set-featured/<type>/<name>')
def set_featrued(type, name):
    if type == 'model':
        model = Model.query.filter_by(id=name).first()
        model.is_featured = True
        db.session.commit()
        flash(f"Model {model.model} updated as featrued model", "success")
        
    elif type == 'article':
        article = Article.query.filter_by(id=name).first()
        article.is_featured = True
        db.session.commit()
        flash(f"Article {article.id} updated as featrued article", "success")
        
    else:
        service = Service.query.filter_by(id=name).first()
        service.is_featured = True
        db.session.commit()
        flash(f"Service {service.title} updated as featured", "success")
    
    return redirect('/admin/dash')

@admin.route('/delete/<type>/<name>')
def delete_model(type, name):
    if type == 'model':
        res = Model.query.filter_by(id=name).first()
        
        shutil.rmtree(f"{static_store}/{res.id}")
        shutil.rmtree(f"{temp_store}/{res.id}")
        
        db.session.delete(res)
        db.session.commit()
        flash(f"Model {name} deleted", "info")
        
    elif type == 'article':
        res = Article.query.filter_by(id=name).first()
        
        shutil.rmtree(f"{temp_article}/{res.id}")
        shutil.rmtree(f"{static_article}/{res.id}")
        
        db.session.delete(res)
        db.session.commit()
        flash(f"Article {res.id} deleted", "info")
        
    elif type == 'service':
        res = Service.query.filter_by(id=name).first()
        
        shutil.rmtree(f"{static_service}/{res.id}")
        shutil.rmtree(f"{temp_service}/{res.id}")
        db.session.delete(res)
        db.session.commit()
        flash(f"Service {res.title} deleted", "info")
        
    else:
        res = Contact.query.filter_by(id=name).first()
        db.session.delete(res)
        db.session.commit()
        flash(f"Feed: {res.topic} from {res.name} deleted", "info")
        
    return redirect('/admin/dash')

# ? Routes
@server.route('/')
def log():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/create-acc')

@server.route('/create-acc', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('create_acc.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_beta = True if request.form.get('is_beta') == 'on' else False
        
        if User.query.filter_by(username=username).first() is not None:
            flash(f"username {username} already exists! Please user another", "error")
            return redirect('/create-acc')
        
        if User.query.filter_by(email=email).first() is not None:
            flash(f"Emal {email} already exists! Try login instead.", "error")
            return redirect('/create-acc')
        
        new_user = User(
            username=username, email=email, password=generate_password_hash(password), is_beta=is_beta
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Your account is created. Now login to your account.", "success")
        return redirect('/login')
    
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            flash(f"username {username} not exists! Try creating account instead", "error")
            return redirect('/login')
        
        if not check_password_hash(user.password, password):
            flash("Invalid Password!", "error")
            return redirect('/login')
        
        login_user(user)
        return redirect('/home')
        
@server.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@server.route('/upgrade-beta')
def upgrade_user():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.is_beta = True
        db.session.commit()
        flash("You are now upgraded to beta user", "success")
    else:
        flash("Login first", 'error')
        
    return redirect('/home')

@server.route('/degrade-beta')
def degrade_user():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.is_beta = False
        db.session.commit()
        flash("You are now degraded from beta user", "info")
    else:
        flash("Login first", 'error')
        
    return redirect('/home')

@server.route('/home')
def home():
    models = Model.query.all()
    articles = Article.query.all()
    return render_template(
        'home.html', models=models, articles=articles
    )

@server.route('/collection')
def collection():
    models = Model.query.all()
    return render_template('collection.html', models=models)

@server.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)

@server.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@server.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        id = str(uuid4())
        name = request.form.get('fullname')
        email = request.form.get('email')
        topic = request.form.get('topic')
        desc = request.form.get('desc')
        
        new_contact = Contact(id=id, name=name, email=email, topic=topic, desc=desc)
        db.session.add(new_contact)
        db.session.commit()
    
        flash("Your query is submitted. Thanks for reaching out to us!", "info")
        return redirect('/home')

@server.route('/overview/<model>')
def show_overview(model):
    html = Model.query.filter_by(id=model).first()
    return render_template(html.overview)

@server.route('/view/<article_id>')
def view_article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    return render_template(article.url)

@server.route('/info/<service_id>')
def show_info(service_id):
    service = Service.query.filter_by(id=service_id).first()
    return render_template(service.info)

# ? Setting up DBs and BPs
with server.app_context():
    db.create_all()
server.register_blueprint(admin)
