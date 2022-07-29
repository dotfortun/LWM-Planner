"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from datetime import datetime, date, time
import random

from apiflask import APIBlueprint
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, User, Pilot, Transaction, Gear,
    Mission, Location, MissionState,
    GearType
)
from api.utils import generate_sitemap, APIException

api = APIBlueprint('api', __name__)


def get_jwt_user():
    return User.query.filter_by(id=get_jwt_identity()).first()

# Users


@api.route("/users", methods=['GET'])
def get_users():
    return jsonify(
        users=[
            user.serialize() for user in User.query.all()
        ]
    )


@api.route("/users/<int:id>", methods=['GET'])
def get_user(id):
    return jsonify(
        user=User.query.filter_by(id=id).first().serialize()
    )


@api.route("/users/active", methods=['GET'])
@jwt_required()
def get_active_user():
    return jsonify(
        user=current_user.serialize()
    )


@api.route("/users/active", methods=['PUT', 'PATCH'])
@jwt_required()
def update_user():
    user = current_user
    if user:
        user.update(**request.get_json())
        db.session.merge(user)
        db.session.commit()
        return jsonify(msg="Success."), 200


@api.route("/users", methods=['POST'])
def post_users():
    """
    {
        "email": <str: email>,
        "password": <str: password>
    }
    """
    if not request.json.get("email", None):
        return jsonify(msg="Missing email"), 400
    if not request.json.get("password", None):
        return jsonify(msg="Missing password"), 400
    if User.query.filter_by(email=request.json.get("email", "")).first():
        return jsonify(msg="User already exists."), 400
    db.session.add(User(
        email=request.json.get("email"),
        password=request.json.get("password"),
    ))
    db.session.commit()
    return jsonify(msg="User created successfully."), 200


@api.route('/login', methods=['POST'])
def login():
    """
    {
        "email": <str: email>,
        "password": <str: password>
    }
    """
    user = User.query.filter_by(email=request.json.get("email", "")).first()
    if user:
        if user.check_password_hash(request.json.get("password", "")):
            return jsonify(token=create_access_token(identity=user)), 200
    return jsonify(msg="Failed to authenticate"), 400

# Pilots


@api.route("/pilots", methods=['GET'])
def get_pilots():
    return jsonify(
        pilots=[x.serialize() for x in Pilot.query.all()]
    )


@api.route("/pilots/<int:id>", methods=['GET'])
def get_pilot(id):
    return jsonify(
        pilot=Pilot.query.filter_by(id=id).first().serialize()
    )


@api.route("/pilots/active", methods=['GET'])
@jwt_required()
def get_active_user_pilots():
    return jsonify(
        pilots=[x.serialize() for x in current_user.pilots]
    )


@api.route("/pilots", methods=['POST'])
@jwt_required()
def post_pilot():
    """
    {
        "name": <str: name>,
        "callsign": <str: callsign>
    }
    """
    user = current_user
    user.pilots.append(Pilot(
        name=request.json.get("name", None),
        callsign=request.json.get("callsign", None)
    ))
    db.session.merge(user)
    db.session.commit()
    return jsonify(msg="Success."), 200

# Missions


@api.route("/missions", methods=['GET'])
def get_missions():
    return jsonify(
        missions=[x.serialize() for x in Mission.query.all()]
    )


@api.route("/missions/<int:id>", methods=['GET'])
def get_mission(id):
    return jsonify(
        mission=Mission.query.filter_by(id=id).first().serialize()
    )


@api.route("/missions", methods=['POST'])
@jwt_required()
def post_mission():
    """
    {
        "name": <str>,
        "description": <str>,
        "difficulty": <int>,
        "is_job?": <bool>,
        "location": <str>
    }
    """
    req = request.get_json()
    if "is_job" in req.keys() and not user.is_admin:
        req["is_job"] = True
    mission = Mission(
        name=req.get("name", None),
        description=req.get("description", None),
        difficulty=req.get("difficulty", 1),
        is_job=req.get("is_job", False),
        location=Location.query.filter_by(
            name=req.get("location", "")).first
    )
    db.session.merge(mission)
    db.session.commit()
    return jsonify(msg="Success."), 200


@api.route("/missions", methods=['PUT', 'PATCH'])
@jwt_required()
def update_mission():
    """
    {
        "id": <int>,
        "name": <str>,
        "description": <str>,
        "difficulty": <int>,
        "is_job": <bool>,
        "location": <str>
    }
    """
    if current_user.is_admin:
        req = request.get_json()
        mission = Mission.query.filter_by(
            id=request.get_json().get("id", None)).first()
        mission.update(req)
        db.session.merge(mission)
        db.session.commit()
        return jsonify(msg="Success."), 200
    return jsonify("Admin Privileges Needed."), 401


@api.route("/missions/join", methods=['POST'])
@jwt_required()
def post_join_mission():
    """
    {
        "pilot": <int: pilot_id>,
        "mission": <int: mission_id>,
        "action": <str: action? ['join', 'leave']>
    }
    """
    req = request.get_json()
    pilot = Pilot.query.filter_by(id=req.get("pilot", None)).first()
    mission = Mission.query.filter_by(id=req.get("mission", None)).first()
    if pilot in current_user.pilots:
        if req.get("action", "join") == "join":
            mission.pilots.append(pilot)
        elif req.get("action", "join") == "leave":
            mission.pilots = list(filter(
                lambda x: x.id != pilot.id,
                mission.pilots
            ))
    db.session.merge(mission)
    db.session.commit()
    return jsonify(msg="Success."), 200

# Locations


@api.route("/locations", methods=['GET'])
def get_locations():
    return jsonify(
        locations=[x.serialize() for x in Location.query.all()]
    )


@api.route("/locations/<int:id>", methods=['GET'])
def get_location(id):
    return jsonify(
        mission=Location.query.filter_by(id=id).first().serialize()
    )


@api.route("/locations", methods=['POST'])
@jwt_required()
def post_location():
    """
    {
        "name": <str>,
        "description": <str>,
        "parent": <str>
    }
    """
    parent = Location.query.filter_by(
        name=request.json.get("parent", "")).first()
    loc = Location(
        name=request.json.get("name", ""),
        description=request.json.get("description", ""),
        parent=parent
    )
    db.session.merge(loc)
    db.session.commit()
    return jsonify(msg="Success."), 200

# Shop methods


@api.route('/store', methods=['GET'])
def get_store():
    seed = int(datetime.combine(date.today(), time(0, 0, 0)).timestamp())
    categories = GearType.query.filter(GearType.value.in_([
        "FRAME", "SYSTEM", "WEAPON", "MOD"
    ])).all()
    resp = {}
    num_choices = {
        "FRAME": 5,
        "SYSTEM": 5,
        "WEAPON": 10,
        "MOD": 2
    }
    for cat in categories:
        random.seed(seed)
        choices = random.choices(
            cat.gear,
            [x.weight for x in cat.gear],
            k=num_choices.get(cat.value, 1)
        )
        items = []
        for item in choices:
            if item.serialize() not in items:
                items.append(item.serialize())
        resp[cat.value] = items
    return jsonify(resp)
