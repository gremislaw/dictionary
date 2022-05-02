from sqlalchemy_serializer import SerializerMixin
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from .db_session import SqlAlchemyBase



class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return f'<Работник> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class LoginForm(FlaskForm, SerializerMixin):
    email = EmailField('Почта', validators=[DataRequired()], render_kw={"placeholder": "Ваша почта"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Ваш пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm, SerializerMixin):
    name = StringField('Имя', validators=[DataRequired()], render_kw={"placeholder": "Ваше имя"})
    surname = StringField('Фамилия', validators=[DataRequired()], render_kw={"placeholder": "Ваша фамилия"})
    email = EmailField('Почта', validators=[DataRequired()], render_kw={"placeholder": "Ваша почта"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Ваш пароль"})
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()],
                                   render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')
