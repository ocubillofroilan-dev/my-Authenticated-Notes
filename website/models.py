from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    # scrypt hashes are ~162 characters long, so 150 was too short for other databases
    password = db.Column(db.String(255), nullable=False)
    fullName = db.Column(db.String(150), nullable=False)
    notes = db.relationship(
        'Note',
        order_by=Note.date.desc(),
        cascade='all, delete-orphan',
    )