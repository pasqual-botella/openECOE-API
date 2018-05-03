from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Student import Student


class StudentResource(ModelResource):
    answers = Relation('option')

    class Meta:
        model = Student
        natural_key = ('name', 'surnames')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        planner = fields.ToOne('planner', nullable=True)
        answers = fields.ToMany('option')
