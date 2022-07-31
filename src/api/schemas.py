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


class TokenSchema(ma.Schema):
    token = af.String()


class PaginationSchema(ma.Schema):
    page = af.Integer(load_default=1)
    per_page = af.Integer(load_default=20, validate=av.Range(max=30))


class UserSchemas:
    class UserIn(ma.SQLAlchemyAutoSchema):
        password = af.String()
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


class PilotSchemas:

    class PilotIn(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Pilot
            load_instance = True

    class PilotOut(ma.SQLAlchemyAutoSchema):
        user = af.Nested('UserOut')
        missions = af.Nested('MissionOut', many=True)
        transactions = af.Nested('InvTransOut', many=True)
        gear = af.Nested('GearOut', many=True)

        class Meta:
            model = Pilot
            include_relationships = True
            load_instance = True

    class PilotsOut(ma.Schema):
        pilots = af.List(af.Nested('PilotOut'))
        pagination = af.Nested(PaginationSchema)


class InvSchema:
    class MultiTransOut(ma.Schema):
        transactions = af.List(af.Nested('InvTransOut'))
        pagination = af.Nested(PaginationSchema)

    class InvItemOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Transaction
            include_relationships = True
            exclude = ("pilot", "is_refunded", "cost")
    
    class InvTransOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Transaction
            include_relationships = False


class GearSchema:
    class InvOut(ma.Schema):
        inventory = af.List(af.Nested('GearOut'))
        pagination = af.Nested(PaginationSchema)
    
    class GearOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Gear
            exclude=("weight",)


class MissionSchema:
    class MissionOut(ma.SQLAlchemyAutoSchema):
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
