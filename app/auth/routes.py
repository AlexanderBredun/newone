from flask import redirect, render_template, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm, PasswordReset, PasswordResetting
from app.models import User
from app import db
from flask_babel import _
from app.auth.email2 import send_password_reset_email
from app.auth import bp


@bp.route('/login', methods = ['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(username = form.username.data).first()
        if user is None:
            flash(_('Invalid username'))
            return redirect(url_for('auth.login'))
        if not user.check_password(form.password.data):
            flash(_('Invalid password'))
            return redirect(url_for('auth.login'))

        login_user(user, remember = form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        return redirect(next_page)

    return render_template('auth/login.html', 
        form = form,
        user = current_user)

@bp.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods = ['GET', 'POST'])

def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Sup my new brother'))

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',
        title = _('Join the gang'),
        form = form,
        user = current_user)

@bp.route('/reset_password_request', methods = ['post', 'get'])

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = PasswordReset()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user:
            send_password_reset_email(user)

        flash(_('check imail'))

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', 
    form = form)

@bp.route('/reset_password/<token>', methods = ['post', 'get'])

def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        redirect(url_for('main.index'))

    form = PasswordResetting()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('succesfull'))
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form = form)