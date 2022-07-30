from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, Location
)
from api.schemas import (
    UserSchemas, PaginationSchema
)
api = APIBlueprint('locations', __name__, url_prefix='/locations')


@api.route("/", methods=['GET'])
def get_locations():
    return jsonify(
        locations=[x.serialize() for x in Location.query.all()]
    )


@api.route("/<int:id>", methods=['GET'])
def get_location(id):
    return jsonify(
        mission=Location.query.filter_by(id=id).first().serialize()
    )


@api.route("/", methods=['POST'])
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
