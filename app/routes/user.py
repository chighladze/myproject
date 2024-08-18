from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user

from ..forms.user import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User
from ..helpers import save_avatar

user = Blueprint('user', __name__)


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.avatar.data)
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data,
                        login=form.login.data,
                        avatar=save_avatar(form.avatar.data),
                        password=hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(str(e))
                flash(f"При регистрации произошла ошибка", "danger")

            flash(f"Пользователь {form.name.data} успешно зарегистрирован", "success")
            return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(login=form.login.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f"Вы успешно авторизованы", "success")
                return redirect(next_page) if next_page else redirect(url_for('post.all'))
            else:
                flash(f"Ошибка входа. Проверьте login и пароль.", "danger")
    return render_template('user/login.html', form=form)


@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))
