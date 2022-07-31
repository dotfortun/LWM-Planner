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
    db, Location
)
from api.schemas import (
    LocationSchemas, PaginationSchema
)
api = APIBlueprint('locations', __name__, url_prefix='/locations')


@api.get("/")
@api.input(PaginationSchema, 'query')
@api.output(LocationSchemas.LocationsOut)
def get_locations(query):
    pagination = Location.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return {
        'locations': pagination.items,
        'pagination': pagination_builder(pagination)
    }


@api.post("/")
@api.input(LocationSchemas.LocationIn)
@api.output(EmptySchema)
@api.doc(summary="Post Location", security="jwt")
@jwt_required()
def post(data):
    loc = Location(
        name=data.get("name", ""),
        description=data.get("description", "")
    )
    db.session.merge(loc)
    db.session.commit()


@api.post("/addrelation")
@api.input(LocationSchemas.RelateIn)
@api.output(EmptySchema)
@api.doc(security="jwt")
@jwt_required()
def add_child(data):
    parent = Location.query(id=data.parent).first()
    child = Location.query(id=data.child).first()
    child.parent = parent
    db.session.merge(child)
    db.session.commit()


@api.route("/<int:id>")
class SingleLocation(MethodView):
    @api.output(LocationSchemas.LocationOut)
    @api.doc(summary="Get Location")
    def get(id):
        return Location.query.filter_by(id=id).first()
