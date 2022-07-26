from app import app
from api.models import db, MissionState
import json

with app.app_context():
    with open('./src/data/missionstate.json', 'rt') as statefile:
        states = json.loads(statefile.read())
        for state in states:
            db.session.add(
                MissionState(
                    name=state["name"],
                    value=state["value"]
                )
            )
        db.session.commit()
        for state in MissionState.query.all():
            json_state = list(filter(
                lambda x: x["value"] == state.value,
                states
            ))[0]
            next_states = MissionState.query.filter(
                MissionState.value.in_([n_state["value"] for n_state in json_state["next"]])
            ).all()
            state.valid_state_changes = next_states
            db.session.merge(state)
        db.session.commit()
