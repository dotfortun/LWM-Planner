from lib2to3.pgen2 import token
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from apiflask import Schema
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


class UserSchemas:
    class UserIn(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = User
            fields = ('email', 'password')

    class UserOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = User
            pilots = af.Nested('PilotSchemas.PilotOut')
            exclude = ('_password', )

    class UsersOut(ma.Schema):
        users = af.List(af.Nested('UserOut'))
        pagination = af.Nested(PaginationSchema)

    class TokenSchema(ma.Schema):
        token = af.String()


class PilotSchemas:
    class PilotIn(ma.Schema):
        name = ma.String()
        callsign = ma.String()

    class PilotOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Pilot

    class PilotsOut(ma.Schema):
        pilots = af.List(af.Nested('PilotOut'))
        pagination = af.Nested(PaginationSchema)


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
