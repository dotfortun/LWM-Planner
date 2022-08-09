"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import jsonify

from apiflask import APIBlueprint, HTTPTokenAuth
from flask_jwt_extended import create_access_token

from api.models import (
    db, User
)
from api.schemas import (
    UserSchemas, TokenSchema
)

import api.api_routes.users as users
import api.api_routes.pilots as pilots
import api.api_routes.missions as missions
import api.api_routes.locations as locations
import api.api_routes.shop as shop

api = APIBlueprint('api', __name__, url_prefix='/api')
api.register_blueprint(users.api)
api.register_blueprint(pilots.api)
api.register_blueprint(missions.api)
api.register_blueprint(locations.api)
api.register_blueprint(shop.api)


@api.route('/login', methods=['POST'])
@api.input(UserSchemas.UserIn)
@api.output(TokenSchema)
def login(data):
    user = User.query.filter_by(
        email=data.get("email", "")).first()
    if user:
        if user.check_password_hash(data.get("password", "")):
            return {"token": create_access_token(identity=user)}
    return jsonify(message="Failed to authenticate"), 400
