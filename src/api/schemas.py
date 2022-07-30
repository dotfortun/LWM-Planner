from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
import apiflask.fields as af
import apiflask.validators as av

from api.models import (
    db, User, Pilot, Transaction, Gear,
    Mission, Location, MissionState,
    GearType, Setting
)

ma = Marshmallow()


class PaginationSchema(ma.Schema):
    page = af.Integer(load_default=1)
    per_page = af.Integer(load_default=20, validate=av.Range(max=30))


class UserOutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('_password', )


class UsersOutSchema(ma.Schema):
    users = af.List(af.Nested(UserOutSchema))
    pagination = af.Nested(PaginationSchema)


class PilotSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pilot


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction


class GearSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gear


class MissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mission


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location


class MissionStateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MissionState


class GearTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GearType


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
