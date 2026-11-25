import re
from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
MIN_PASSWORD_LENGTH = 8
# Used to compare against when the email doesn't exist, so a login attempt takes
# about the same time either way.
DUMMY_HASH = generate_password_hash('not-a-real-password')


def is_safe_next_url(target):
    """Only allow redirects to paths on this site (prevents open redirects)."""
    if not target:
        return False
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and target.startswith('/') and not target.startswith('//')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.notes'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()
        password_ok = check_password_hash(user.password if user else DUMMY_HASH, password)

        if user and password_ok:
            login_user(user, remember=remember)
            flash('Logged in successfully!', category='success')
            next_url = request.args.get('next')
            return redirect(next_url if is_safe_next_url(next_url) else url_for('views.notes'))

        # Same message for both cases so nobody can find out which emails are registered.
        flash('Invalid email or password.', category='error')

    return render_template('login.html')


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.notes'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        full_name = (request.form.get('fullName') or '').strip()
        password1 = request.form.get('password1') or ''
        password2 = request.form.get('password2') or ''

        if not EMAIL_PATTERN.match(email) or len(email) > 150:
            flash('Please enter a valid email address.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        elif len(full_name) < 2:
            flash('Full name must be at least 2 characters.', category='error')
        elif len(full_name) > 150:
            flash('Full name is too long.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < MIN_PASSWORD_LENGTH:
            flash(f'Password must be at least {MIN_PASSWORD_LENGTH} characters.', category='error')
        else:
            new_user = User(
                email=email,
                fullName=full_name,
                password=generate_password_hash(password1),
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.notes'))

    return render_template('sign_up.html')