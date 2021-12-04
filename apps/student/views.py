from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user


from exts import db
from form import RegisterForm, LoginForm
from model import User

student_bp = Blueprint('student', __name__)


@student_bp.route('/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('base.html')
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        password = form.password.data
        repassword = form.password.data
        if_registe = User.query.filter_by(email=email)
        if not if_registe:
                # repassword = form.repassword.data
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return render_template('test.html')
        else:
            flash('The account has been registed', 'warning')
            return redirect(url_for('student.register'))
        # else:
        #     flash('You should input same password', 'warning')
        #     return redirect(url_for('student.register'))
    return render_template('auth/register_.html', form=form)


@student_bp.route('/login', methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('student.'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember.data):
                flash('Login success.', 'info')

                from flask import current_app
                current_app.logger.info(user.username+'Login Successfully.')
                current_app.logger.warning(user.username + 'Login Successfully.')
                current_app.logger.error(user.username + 'Login Successfully.')
                current_app.logger.debug(user.username + 'Login Successfully.')
                return redirect(url_for('main.index', username=form.username.data))
            else:
                flash('Your account is blocked.', 'warning')
                return render_template('auth/login_.html')
        flash('Invalid email or password.', 'warning')
    return render_template('auth/login_.html', form=form)


@student_bp.route('/background')
def background():
    return render_template('background.html')


@student_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('student.login'))
