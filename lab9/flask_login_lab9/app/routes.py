from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('base.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.account'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html', form=form)


@main.route('/account')
@login_required
def account():
    return render_template('account.html')


@main.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

