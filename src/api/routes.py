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


@api.route("/users", methods=['GET'])
def get_users():
    return jsonify(
        users=[
            user.serialize() for user in User.query.all()
        ]
    )

@api.route("/pilots/<int:id>", methods=['GET'])
def get_pilot(id):
    return jsonify(
        pilot=Pilot.query.filter_by(id=id).first().serialize()
    )


@api.route("/missions/<int:id>", methods=['GET'])
def get_mission(id):
    return jsonify(
        pilot=Mission.query.filter_by(id=id).first().serialize()
    )

