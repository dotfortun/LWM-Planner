from datetime import datetime, date, time
import random

from apiflask import APIBlueprint, pagination_builder
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token, current_user
)

from api.models import (
    db, GearType, Pilot, Transaction, Gear
)
from api.schemas import (
    UserSchemas, PaginationSchema
)
api = APIBlueprint('shop', __name__, url_prefix='/shop')


@api.route('/', methods=['GET'])
def get_store():
    seed = int(datetime.combine(date.today(), time(0, 0, 0)).timestamp())
    categories = GearType.query.filter(GearType.value.in_([
        "FRAME", "SYSTEM", "WEAPON", "MOD"
    ])).all()
    resp = {}
    num_choices = {
        "FRAME": 5,
        "SYSTEM": 5,
        "WEAPON": 10,
        "MOD": 2
    }
    for cat in categories:
        random.seed(seed)
        choices = random.choices(
            cat.gear,
            [x.weight for x in cat.gear],
            k=num_choices.get(cat.value, 1)
        )
        items = []
        for item in choices:
            if item.serialize() not in items:
                items.append(item.serialize())
        resp[cat.value.lower()] = items
    return jsonify(shop_items=resp)


@api.route("/purchase", methods=['POST'])
@jwt_required()
def make_purchase():
    """
    {
        "pilot_id": <int: pilot id>,
        "item_id": <int: item id>
    }
    """
    pilot = Pilot.query.filter_by(id=request.get_json()["pilot_id"]).first()
    item = Gear.query.filter_by(id=request.get_json()["item_id"]).first()
    pilot.transactions.append(
        Transaction(item=item, pilot=pilot)
    )
    db.session.merge(pilot)
    db.session.commit()
    return jsonify(msg="Success"), 200
