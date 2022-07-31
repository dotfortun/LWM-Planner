from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from apiflask.schemas import EmptySchema
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, Mission, Location, Pilot
)
from api.schemas import (
    MissionSchemas, PaginationSchema
)
api = APIBlueprint('missions', __name__, url_prefix='/missions')


@api.route("/<int:id>")
class SingleMission(MethodView):
    @api.output(MissionSchemas.MissionOut)
    @api.doc(summary="Get Mission")
    def get(self, id):
        return Mission.query.filter_by(id=id).first()

    @api.input(MissionSchemas.MissionIn)
    @api.output(EmptySchema)
    @api.doc(summary="Put Mission", security="jwt")
    @jwt_required()
    def put(self):
        if current_user.is_admin:
            req = request.get_json()
            mission = Mission.query.filter_by(id=id).first()
            mission.update(req)
            db.session.merge(mission)
            db.session.commit()
            return jsonify(message="Success."), 200
        return jsonify("Admin Privileges Needed."), 401


@api.post("/")
@api.input(MissionSchemas.MissionIn)
@api.output(EmptySchema)
@api.doc(summary="Post Mission", security="jwt")
@jwt_required()
def post(self):
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


@api.get("/")
@api.input(PaginationSchema, 'query')
@api.output(MissionSchemas.MissionsOut)
def get_missions(query):
    pagination = Mission.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return {
        'missions': pagination.items,
        'pagination': pagination_builder(pagination)
    }


@api.route("/join", methods=['POST'])
@api.input(MissionSchemas.Join)
@api.output(EmptySchema)
@api.doc(security="jwt")
@jwt_required()
def join_mission():
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
