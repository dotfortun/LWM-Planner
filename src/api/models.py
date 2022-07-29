from datetime import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
ma = Marshmallow()

user_to_pilot = db.Table(
    "user_to_pilot",
    db.metadata,
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey('user.id')
    ),
    db.Column(
        "pilot_id",
        db.Integer,
        db.ForeignKey('pilot.id')
    ),
)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True,
                      nullable=False, primary_key=True)
    _password = db.Column(db.String(128), unique=False, nullable=False)
    is_active = db.Column(
        db.Boolean(),
        default=True
    )
    is_admin = db.Column(
        db.Boolean(),
        default=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "pilots": [pilot.serialize() for pilot in self.pilots]
        }

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class Setting(db.Model):
    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    key = db.Column(db.String(120), primary_key=True)
    setting = db.Column(db.JSON, default=None)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


pilot_to_mission = db.Table(
    "pilot_to_mission",
    db.metadata,
    db.Column(
        "pilot_id",
        db.Integer,
        db.ForeignKey('pilot.id')
    ),
    db.Column(
        "mission_id",
        db.Integer,
        db.ForeignKey('mission.id')
    ),
)


class Pilot(db.Model):
    __tablename__ = "pilot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    callsign = db.Column(db.String(120), nullable=True)
    hull = db.Column(db.Integer, default=0)
    agility = db.Column(db.Integer, default=0)
    systems = db.Column(db.Integer, default=0)
    engineering = db.Column(db.Integer, default=0)
    manna = db.Column(db.Integer, default=1000)
    missions = db.relationship(
        "Mission",
        secondary=pilot_to_mission,
        primaryjoin=(id == pilot_to_mission.c.pilot_id),
        uselist=True,
        backref="pilots"
    )
    user = db.relationship(
        "User",
        secondary=user_to_pilot,
        primaryjoin=(id == user_to_pilot.c.pilot_id),
        uselist=False,
        backref="pilots"
    )

    def __repr__(self):
        return '<Pilot {}>'.format(self.callsign)

    @property
    def grit(self):
        return sum([self.hull, self.agility,
                    self.systems, self.engineering]) // 2

    @property
    def gear(self):
        return [
            transaction.item for transaction in filter(
                lambda x: not x.is_refunded,
                self.transactions
            )
        ]

    @property
    def frames(self):
        return [
            transaction.item for transaction in filter(
                lambda x: not x.is_refunded and x.item.gear_type.value == "FRAME",
                self.transactions
            )
        ]

    def serialize(self, no_recurse=False, abridge=False):
        if abridge:
            return {
                "id": self.id,
                "pilot": self.name
            }
        if no_recurse:
            return {
                "id": self.id,
                "name": self.name,
                "callsign": self.callsign,
                "hase": {
                    "hull": self.hull,
                    "agility": self.agility,
                    "systems": self.systems,
                    "engineering": self.engineering,
                },
                "grit": self.grit,
                "manna": self.manna,
            }
        return {
            "id": self.id,
            "name": self.name,
            "callsign": self.callsign,
            "hase": {
                "hull": self.hull,
                "agility": self.agility,
                "systems": self.systems,
                "engineering": self.engineering,
            },
            "grit": self.grit,
            "manna": self.manna,
            "gear": [
                x.serialize() for x in self.gear
            ],
            "frames": [
                x.serialize(desc=False) for x in self.frames
            ],
            "transactions": [
                x.serialize() for x in self.transactions
            ],
            "missions": [
                x.serialize() for x in self.missions
            ]
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


class GearType(db.Model):
    __tablename__ = "gear_type"
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    value = db.Column(db.String(120), nullable=True,
                      unique=True, primary_key=True)
    name = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<GearType {}>'.format(self.name)


class Gear(db.Model):
    __tablename__ = "gear"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey("gear_type.id"))
    weight = db.Column(db.Float, default=0.0)
    gear_type = db.relationship(
        "GearType",
        uselist=False,
        backref="gear"
    )

    def __repr__(self):
        return '<Gear {}>'.format(self.name)

    def serialize(self, desc=True):
        if desc:
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description
            }
        return {
            "id": self.id,
            "name": self.name
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("gear.id"))
    pilot_id = db.Column(db.Integer, db.ForeignKey("pilot.id"))
    is_refunded = db.Column(db.Boolean, default=False)
    item = db.relationship(
        "Gear",
        uselist=False
    )
    pilot = db.relationship(
        "Pilot",
        uselist=False,
        backref="transactions"
    )

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

    def serialize(self):
        return {
            "item": self.item.serialize(desc=False),
            "cost": self.cost,
            "pilot": self.pilot.serialize(no_recurse=True),
            "is_refunded": self.is_refunded,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


mission_to_loot = db.Table(
    "mission_to_loot",
    db.metadata,
    db.Column(
        "mission_id",
        db.Integer,
        db.ForeignKey('mission.id')
    ),
    db.Column(
        "gear_id",
        db.Integer,
        db.ForeignKey('gear.id')
    ),
)


class Mission(db.Model):
    __tablename__ = "mission"
    id = db.Column(db.Integer, primary_key=True)
    gm_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Integer, default=1)
    is_job = db.Column(db.Boolean, default=True)
    schedule = db.Column(db.DateTime, default=datetime.now())
    state_id = db.Column(db.Integer, db.ForeignKey(
        "mission_state.id"), nullable=True)
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id")
    )
    loot = db.relationship(
        "Gear",
        secondary=mission_to_loot,
        primaryjoin=(id == mission_to_loot.c.mission_id),
        uselist=True
    )
    location = db.relationship(
        "Location",
        uselist=False,
        backref="mission_history"
    )
    mission_state = db.relationship(
        "MissionState",
        uselist=False
    )
    gm = db.relationship(
        "User",
        uselist=False
    )

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "is_job": self.is_job,
            "scheduled_date": self.schedule,
            "pilots": [
                x.serialize(abridge=True) for x in self.pilots
            ],
            "loot": [
                x.serialize(desc=False) for x in self.loot
            ],
            "location": self.location.serialize(),
            "mission_state": {
                "name": self.mission_state.name,
                "value": self.mission_state.value
            },
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


location_tree = db.Table(
    "location_tree",
    db.metadata,
    db.Column(
        "parent",
        db.Integer,
        db.ForeignKey('location.id')
    ),
    db.Column(
        "child",
        db.Integer,
        db.ForeignKey('location.id')
    ),
)


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    parent = db.relationship(
        "Location",
        secondary=location_tree,
        primaryjoin=(id == location_tree.c.child),
        secondaryjoin=(id == location_tree.c.parent),
        uselist=False,
        backref="child_locations"
    )

    def __repr__(self):
        return '<Location {}>'.format(self.name)

    def serialize(self):
        parent = None
        if self.parent:
            parent = self.parent.name
        return {
            "name": self.name,
            "description": self.description,
            "parent": parent,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)


mission_state_changes = db.Table(
    "mission_state_changes",
    db.metadata,
    db.Column(
        "current_state",
        db.Integer,
        db.ForeignKey('mission_state.id')
    ),
    db.Column(
        "next_state",
        db.Integer,
        db.ForeignKey('mission_state.id')
    ),
)


class MissionState(db.Model):
    __tablename__ = "mission_state"
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    value = db.Column(db.String(120), nullable=True,
                      unique=True, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    prev = db.relationship(
        "MissionState",
        secondary=mission_state_changes,
        primaryjoin=(id == mission_state_changes.c.next_state),
        secondaryjoin=(id == mission_state_changes.c.current_state),
        uselist=False,
        backref="valid_state_changes"
    )

    def __repr__(self):
        return '<MissionState {}>'.format(self.value)

    def serialize(self, prev=False):
        if not prev:
            return {
                "value": self.value,
                "name": self.name,
                "next": [
                    x.serialize() for x in self.valid_state_changes
                ],
            }
        prev = None
        if self.prev:
            prev = self.prev.name
        return {
            "value": self.value,
            "name": self.name,
            "prev": prev,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
