from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.routes import Relation
from app.model.Station import Station
from .ecoe import EcoePrincipalResource


class StationResource(EcoePrincipalResource):
    schedules = Relation('schedules')
    qblocks = Relation('qblocks')

    class Meta:
        name = 'stations'
        model = Station
        natural_key = ('ecoe', 'name')

        permissions = {
            'read': 'manage',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage:ecoe', 'manage', 'user:user']
        }

    class Schema:
        ecoe = fields.ToOne('ecoes')
        user = fields.ToOne('users', nullable=True)
        parent_station = fields.ToOne('stations', nullable=True)
        children_stations = fields.ToMany('stations', nullable=True)


def order_station(item, op='add'):
    order_correction = 0

    stations_ecoe = len(item.ecoe.stations)
    if not item.order or item.order > stations_ecoe or item.order < 1:
        item.order = stations_ecoe
    else:
        stations_ecoe = Station.query \
            .filter(Station.id_ecoe == item.ecoe.id).filter(Station.order >= item.order) \
            .filter(Station.id != item.id).order_by(Station.order).all()

        if op == 'add':
            order_correction = 1

        for order, station_ecoe in enumerate(stations_ecoe):
            station_ecoe.order = order + item.order + order_correction


@signals.before_update.connect_via(StationResource)
def before_update_station(sender, item, changes):
    if 'order' in changes.keys():
        item.order = changes['order']
        order_station(item)


# TODO: Review Create Station Order
# Add permissions to manage to creator
@signals.before_create.connect_via(StationResource)
def before_create_station(sender, item):
    # order_station(item)
    if not item.user:
        item.user = current_user


@signals.before_delete.connect_via(StationResource)
def before_delete_station(sender, item):
    order_station(item, 'del')
