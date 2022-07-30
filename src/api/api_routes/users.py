from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, User
)
from api.schemas import (
    UserSchemas, PaginationSchema
)
from api.utils import generate_sitemap, APIException
api = APIBlueprint('users', __name__, url_prefix='/users')


@api.route("/")
class UserRoutes(MethodView):
    @api.input(PaginationSchema, 'query')
    @api.output(UserSchemas.UsersOut)
    def get(query):
        pagination = User.query.paginate(
            page=query['page'],
            per_page=query['per_page']
        )
        users = pagination.items
        return {
            'users': users,
            'pagination': pagination_builder(pagination)
        }

    @api.input(UserSchemas.UserIn)
    def post():
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


@api.get("/<int:id>")
@api.input(UserSchemas.UserIn)
@api.output(UserSchemas.UserOut)
def get_user(id):
    return jsonify(
        user=User.query.filter_by(id=id).first().serialize()
    )


@api.route("/active")
@jwt_required()
@api.doc(security='BearerAuth')
class Active_User_Routes(MethodView):
    @api.output(UserSchemas.UserOut)
    def get(self):
        return jsonify(
            user=current_user.serialize()
        )

    def put(self):
        if current_user:
            current_user.update(**request.get_json())
            db.session.merge(current_user)
            db.session.commit()
            return jsonify(message="Success."), 200
