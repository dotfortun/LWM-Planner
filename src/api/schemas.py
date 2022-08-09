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
        email = af.String(required=True)
        password = af.String(required=True)
        class Meta:
            model = User
            fields = ('email', 'password')

    class UserUpdate(ma.SQLAlchemyAutoSchema):
        email = af.String(required=False)
        password = af.String(required=False)
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

    class PilotIn(ma.SQLAlchemySchema):
        name = ma.String(required=False)
        callsign = ma.String(required=False)
        hull = ma.Integer(required=False)
        agility = ma.Integer(required=False)
        systems = ma.Integer(required=False)
        engineering = ma.Integer(required=False)
        manna = ma.Integer(required=False)

        class Meta:
            model = Pilot

    class PilotOut(ma.SQLAlchemyAutoSchema):
        user = af.Nested('UserOut')
        missions = af.Nested('MissionOut', many=True)
        transactions = af.Nested('InvTransOut', many=True)
        gear = af.Nested('GearOut', many=True)

        class Meta:
            model = Pilot
            include_relationships = True
            load_instance = True

    class PilotOutShort(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Pilot
            exclude = (
                "agility",
                "engineering",
                "hull",
                "manna",
                "systems",
            )

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


class MissionSchemas:
    class MissionsOut(ma.Schema):
        missions = af.List(af.Nested('MissionOut'))
        pagination = af.Nested(PaginationSchema)

    class MissionOut(ma.SQLAlchemyAutoSchema):
        location = ma.Nested('LocationOut')
        loot = af.Nested('GearOut', many=True)
        pilots = af.Nested('PilotOutShort', many=True)
        gm = af.Nested('UserOut')
        mission_state = ma.Nested('MissionStateOut')

        class Meta:
            model = Mission
            include_relationships = True

    class MissionIn(ma.SQLAlchemySchema):
        name = ma.String(required=False)
        description = ma.String(required=False)
        difficulty = ma.Integer(required=False)
        is_job = ma.Boolean(required=False)
        schedule = ma.DateTime(required=False)
        gm_id = ma.Integer(required=False)
        location_id = ma.Integer(required=False)
        state_id = ma.Integer(required=False)

        class Meta:
            model = Mission

    class Join(ma.Schema):
        pilot_id = ma.Integer()
        mission_id = ma.Integer()


class LocationSchemas:
    class LocationsOut(ma.Schema):
        locations = af.List(af.Nested('LocationOut'))
        pagination = af.Nested(PaginationSchema)

    class LocationOut(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Location
    
    class LocationIn(ma.SQLAlchemySchema):
        name = ma.String(required=False)
        description = ma.String(required=False)

        class Meta:
            model = Location

    class RelateIn(ma.Schema):
        parent = ma.Integer()
        child = ma.Integer()



class MissionStateOut(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MissionState
        exclude = ("id", )


class GearTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GearType
        exclude = ("id", )


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
        exclude = ("id", )
