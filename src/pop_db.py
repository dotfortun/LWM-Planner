from app import app
from api.models import db, MissionState
import json

with app.app_context():
    with open("./src/data/missionstate.json", "rt") as statefile:
        states = json.loads(statefile.read())
        for state in states:
            db.session.add(
                MissionState(name=state["name"], value=state["value"]))
        db.session.commit()
        for state in MissionState.query.all():
            json_state = list(
                filter(lambda x: x["value"] == state.value, states))[0]
            state.prev = MissionState.query.filter_by(
                prev=json_state["prev"]).first()
            db.session.merge(state)
        db.session.commit()
