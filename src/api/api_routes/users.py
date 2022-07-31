from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, HTTPTokenAuth, pagination_builder
from apiflask.schemas import EmptySchema
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, User, Pilot
)
from api.schemas import (
    UserSchemas, PaginationSchema, GearSchema, PilotSchemas
)
api = APIBlueprint('users', __name__, url_prefix='/users')


@api.get("/")
@api.input(PaginationSchema, 'query')
@api.output(UserSchemas.UsersOut)
def get_users(query):
    pagination = User.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return {
        'users': pagination.items,
        'pagination': pagination_builder(pagination)
    }


@api.post("/")
@api.input(UserSchemas.UserIn, 'query')
@api.output(EmptySchema)
def post_user(query):
    if not query.get("email", None):
        return jsonify(message="Missing email"), 400
    if not query.get("password", None):
        return jsonify(message="Missing password"), 400
    if User.query.filter_by(email=query.get("email", "")).first():
        return jsonify(message="User already exists."), 400
    db.session.add(User(
        email=query.get("email"),
        password=query.get("password"),
    ))
    db.session.commit()


@api.get("/<int:id>")
@api.output(UserSchemas.UserOut)
def get_user(id):
    return jsonify(
        user=User.query.filter_by(id=id).first().serialize()
    )


@api.route("/active")
class ActiveUser(MethodView):
    decorators = [jwt_required(), api.doc(security='jwt')]

    @api.output(UserSchemas.UserOut)
    def get(self):
        return current_user

    @api.input(UserSchemas.UserUpdate)
    @api.output(UserSchemas.UserOut)
    def put(self, data):
        current_user.update(**request.get_json())
        db.session.merge(current_user)
        db.session.commit()
        return User.query.filter_by(id=current_user.id).first()

    @api.get("/pilots")
    @api.output(PilotSchemas.PilotsOut)
    @api.doc(security='jwt')
    @jwt_required()
    def get_active_user_pilots():
        return jsonify(
            pilots=[x.serialize() for x in current_user.pilots]
        )

    @api.get("/pilots/<int:pilotid>")
    @api.output(PilotSchemas.PilotOut)
    @api.doc(security='jwt')
    @jwt_required()
    def get_active_user_pilot(pilot_id):
        return Pilot.query.filter_by(
            user=current_user,
            id=pilot_id
        ).first()
