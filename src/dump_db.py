from app import app
from api.models import MissionState, Location
import json

with app.app_context():
    states = []
    for state in MissionState.query.all():
        states.append(state.serialize(prev=True))
    with open('./src/data/missionstate.json', 'wt') as statefile:
        statefile.write(
            json.dumps(states)
        )
    locations = []
    for location in Location.query.all():
        locations.append(location.serialize())
    with open('./src/data/locations.json', 'wt') as statefile:
        statefile.write(
            json.dumps(locations)
        )
