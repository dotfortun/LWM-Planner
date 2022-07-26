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