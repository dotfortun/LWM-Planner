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
    PaginationSchema, PilotSchemas
)
api = APIBlueprint('pilots', __name__, url_prefix='/pilots')


@api.route("/<int:id>", methods=['GET'])
def get_pilot(id):
    return jsonify(
        pilot=Pilot.query.filter_by(id=id).first().serialize()
    )


@api.route("/")
class Pilots(MethodView):
    @api.input(PaginationSchema, 'query')
    @api.output(PilotSchemas.PilotsOut)
    def get(self, query):
        pagination = Pilot.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        return {
            'pilots': pagination.items,
            'pagination': pagination_builder(pagination)
        }

    @api.input(PilotSchemas.PilotIn)
    @api.output(PilotSchemas.PilotOut)
    @api.doc(security="jwt")
    @jwt_required()
    def post(self, data):
        user = current_user
        user.pilots.append(Pilot(
            name=data.get("name", None),
            callsign=data.get("callsign", None)
        ))
        db.session.merge(user)
        db.session.commit()
        return Pilot.query.filter_by(
            name=data.get("name", None),
            callsign=data.get("callsign", None)
        ).first()
