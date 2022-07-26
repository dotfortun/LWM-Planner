"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from api.models import (
    db, User, Pilot, Transaction, Gear,
    Mission, Location, MissionState
)
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

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
        pilot=User.query.filter_by(id=id).first().serialize()
    )


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
    user = User.query.filter_by(request.json.get("email", "")).first()
    if user:
        if user.check_password_hash(request.json.get("password", "")):
            return jsonify(token=create_access_token(identity=user.id)), 200
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


@jwt_required()
@api.route("/pilots", methods=['POST'])
def post_pilot():
    """
    {
        "name": <str: name>,
        "callsign": <str: callsign>
    }
    """
    user = User.query.filter_by(id=get_jwt_identity()).first()
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
        missiosn=[x.serialize() for x in Mission.query.all()]
    )


@api.route("/missions/<int:id>", methods=['GET'])
def get_mission(id):
    return jsonify(
        mission=Mission.query.filter_by(id=id).first().serialize()
    )


@jwt_required()
@api.route("/missions", methods=['POST'])
def post_mission():
    return jsonify(
        pilot=Mission.query.filter_by(id=id).first().serialize()
    )

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


@jwt_required()
@api.route("/locations", methods=['POST'])
def post_location():
    return jsonify(
        pilot=Location.query.filter_by(id=id).first().serialize()
    )
