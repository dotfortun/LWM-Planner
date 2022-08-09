from app import app
from api.models import (User, Pilot, MissionState, Location, Mission)
from api.schemas import MissionSchemas
import json

with app.app_context():
    missions = []
    for mission in Mission.query.all():
        missions.append(MissionSchemas.MissionIn().dump(mission))
    with open('./src/data/missions.json', 'wt') as mission_file:
        mission_file.write(
            json.dumps(missions)
        )
    # states = []
    # for state in MissionState.query.all():
    #     states.append(state.serialize(prev=True))
    # with open('./src/data/missionstate.json', 'wt') as statefile:
    #     statefile.write(
    #         json.dumps(states)
    #     )
    # locations = []
    # for location in Location.query.all():
    #     locations.append(location.serialize())
    # with open('./src/data/locations.json', 'wt') as statefile:
    #     statefile.write(
    #         json.dumps(locations)
    #     )
