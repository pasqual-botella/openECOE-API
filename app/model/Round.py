from app import db
from .Shift import Shift

from sqlalchemy.orm import backref


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    id_shift = db.Column(db.Integer, db.ForeignKey(Shift.id), nullable=False)
    shift = db.relationship(Shift, backref=backref('rounds', lazy='dynamic'))