import os
import secrets

from flask import Flask, flash, jsonify, redirect, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

DB_NAME = "database.db"


def load_secret_key(app):
    """Use the SECRET_KEY environment variable if set, otherwise create a random
    key once and keep it in instance/secret_key (so logins survive restarts)."""
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key

    key_file = os.path.join(app.instance_path, 'secret_key')
    if os.path.exists(key_file):
        with open(key_file, 'r', encoding='utf-8') as f:
            return f.read().strip()

    key = secrets.token_hex(32)
    with open(key_file, 'w', encoding='utf-8') as f:
        f.write(key)
    return key


def create_app():
    app = Flask(__name__)
    os.makedirs(app.instance_path, exist_ok=True)

    app.config['SECRET_KEY'] = load_secret_key(app)
    # Uses DATABASE_URL (e.g. a Postgres database on Render) if set,
    # otherwise a local SQLite file inside the "instance" folder.
    database_url = os.environ.get('DATABASE_URL', f'sqlite:///{DB_NAME}')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
    # Render sets the RENDER variable; there we serve over HTTPS, so cookies can be secure.
    on_render = bool(os.environ.get('RENDER'))
    app.config['SESSION_COOKIE_SECURE'] = on_render
    app.config['REMEMBER_COOKIE_SECURE'] = on_render

    db.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to see that page.'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @app.errorhandler(CSRFError)
    def handle_csrf_error(_error):
        if request.is_json:
            return jsonify(error='Your session expired. Please refresh the page.'), 400
        flash('Your session expired. Please try again.', category='error')
        return redirect(url_for('views.notes'))

    with app.app_context():
        db.create_all()  # only creates tables that don't exist yet

    return app