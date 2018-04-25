from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('area')
    days = Relation('day')
    students = Relation('student')

    class Meta:
        model = ECOE
        natural_key = ('name')

    class Schema:
        organization = fields.ToOne('organization')
        chronometers = fields.ToMany('chronometer')
