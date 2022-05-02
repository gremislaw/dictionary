from .db_session import SqlAlchemyBase
import sqlalchemy
from flask import jsonify, redirect, request
from data import db_session

from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired



class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'words'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pometa = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    s_pometoi = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translate = sqlalchemy.Column(sqlalchemy.String, nullable=True)


def search_word(name):
    db_sess = db_session.create_session()
    words = db_sess.query(Word).filter_by(name=name).first()
    if not words:
        return redirect(f"/words/0")
    return redirect(f"/words/{name}")


def add_new_word(name, about, translate):
    db_sess = db_session.create_session()
    word = Word(
        name=name,
        about=about,
        translate=translate
    )
    db_sess.add(word)
    db_sess.commit()


