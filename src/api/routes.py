"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
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

@api.route("/pilots", methods=['POST'])
def post_pilot():
    return jsonify(
        pilot=Pilot.query.filter_by(id=id).first().serialize()
    )

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

# Locations

@api.route("/locations/<int:id>", methods=['GET'])
def get_location(id):
    return jsonify(
        mission=Location.query.filter_by(id=id).first().serialize()
    )

@api.route("/locations", methods=['GET'])
def get_locations():
    return jsonify(
        locations=[x.serialize() for x in Location.query.all()]
    )

