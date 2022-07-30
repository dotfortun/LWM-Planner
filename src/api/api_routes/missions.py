from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, Mission, Location, Pilot
)
from api.schemas import (
    UserSchemas, PaginationSchema
)
from api.utils import generate_sitemap, APIException
api = APIBlueprint('missions', __name__, url_prefix='/missions')


@api.route("/", methods=['GET'])
def get_missions():
    return jsonify(
        missions=[x.serialize() for x in Mission.query.all()]
    )


@api.route("/<int:id>", methods=['GET'])
def get_mission(id):
    return jsonify(
        mission=Mission.query.filter_by(id=id).first().serialize()
    )


@api.route("/", methods=['POST'])
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
    if "is_job" in req.keys() and not current_user.is_admin:
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


@api.route("/", methods=['PUT', 'PATCH'])
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


@api.route("/join", methods=['POST'])
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
