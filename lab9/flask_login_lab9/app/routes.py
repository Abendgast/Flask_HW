import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import RegisterForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from app.models import User

main = Blueprint('main', __name__)


def save_picture(form_picture):
    """
    Зберігає оригінал і створює thumbnail 128x128 з суфіксом _thumb
    Повертає ім'я збереженого файлу (оригіналу).
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    f_ext = f_ext.lower()
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    # зберегти оригінал
    form_picture.stream.seek(0)
    form_picture.save(picture_path)

    # створити thumb 128x128
    thumb_fn = random_hex + '_thumb' + f_ext
    thumb_path = os.path.join(current_app.config['UPLOAD_FOLDER'], thumb_fn)

    img = Image.open(picture_path)
    img.thumbnail((128, 128))
    img.save(thumb_path)

    return picture_fn, thumb_fn


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
        # image, about_me and last_seen use defaults
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


@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    upd_form = UpdateAccountForm(prefix='upd')
    pwd_form = ChangePasswordForm(prefix='pwd')

    # наповнення полів форми поточними значеннями
    if request.method == 'GET':
        upd_form.username.data = current_user.username
        upd_form.email.data = current_user.email
        upd_form.about_me.data = current_user.about_me

    # Обробка оновлення акаунту
    if upd_form.validate_on_submit() and upd_form.submit.data:
        # файл картинки (опціонально)
        if upd_form.picture.data:
            picture_file, thumb_file = save_picture(upd_form.picture.data)
            # зберігаємо ім'я файлу у User.image (зберігаємо оригінал; thumb можна використовувати за потреби)
            current_user.image = picture_file

        current_user.username = upd_form.username.data
        current_user.email = upd_form.email.data
        current_user.about_me = upd_form.about_me.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('main.account'))

    # Обробка зміни пароля
    if pwd_form.validate_on_submit() and pwd_form.submit.data:
        if not current_user.check_password(pwd_form.old_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(pwd_form.new_password.data)
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('main.account'))

    return render_template('account.html', upd_form=upd_form, pwd_form=pwd_form, user=current_user)


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

