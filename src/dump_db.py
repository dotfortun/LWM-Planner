from app import app
from api.models import MissionState
import json

with app.app_context():
    states = []
    for state in MissionState.query.all():
        states.append(state.serialize())
    with open('./src/data/missionstate.json', 'wt') as statefile:
        statefile.write(
            json.dumps(states)
        )
