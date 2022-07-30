from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, Pilot
)
from api.schemas import (
    PaginationSchema
)
from api.utils import generate_sitemap, APIException
api = APIBlueprint('pilots', __name__, url_prefix='/pilots')


@api.route("/", methods=['GET'])
def get_pilots():
    return jsonify(
        pilots=[x.serialize() for x in Pilot.query.all()]
    )


@api.route("/<int:id>", methods=['GET'])
def get_pilot(id):
    return jsonify(
        pilot=Pilot.query.filter_by(id=id).first().serialize()
    )


@api.route("/active", methods=['GET'])
@jwt_required()
def get_active_user_pilots():
    return jsonify(
        pilots=[x.serialize() for x in current_user.pilots]
    )


@api.route("/", methods=['POST'])
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
