from flask import Flask, request, url_for, redirect, render_template, jsonify, make_response, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session, words_api
from flask_ngrok import run_with_ngrok
from data.word import Word, search_word, add_new_word
from data.users import User, LoginForm, RegisterForm
import datetime




app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JSON_AS_ASCII'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/database.db")
    app.register_blueprint(words_api.blueprint)

# passwords
#   "cap"
#   "sci"
#   "bio"
#   "pilot"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('main_menu.html', title='Главная страница')
    elif request.method == 'POST':
        if request.form['some_button'] == 'add_word':
            name_new = request.form['new_word_name'].capitalize()
            about_new = request.form['new_word_about'].lower()
            translate_new = request.form['new_word_translate'].lower()
            if 25 < len(name_new) or len(name_new) < 2:
                flash("Длина названия должна быть больше 1 и меньше 25", 'error')
            elif 100 < len(about_new) or len(about_new) < 2:
                flash("Длина значения должна быть больше 1 и меньше 100", 'error')
            elif 25 < len(translate_new) or len(translate_new) < 1:
                flash("Длина перевода должна быть больше 0 и меньше 25", 'error')
            else:
                add_new_word(name_new, about_new, translate_new)
                flash("Слово успешно добавлено", 'success')
            return render_template('main_menu.html', title='Главная страница')
        name = request.form['search'].capitalize()
        return search_word(name)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли в систему", 'success')
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают.")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=f'{user.email} уже зарегистрирована.')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            admin=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash("Вы успешно зарегистрированы в системе", 'success')
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
    run_with_ngrok(app)
    app.run()