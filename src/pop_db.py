from app import app
from api.models import db, MissionState, Location
import json

with app.app_context():
    with open("./src/data/missionstate.json", "rt") as statefile:
        states = json.loads(statefile.read())
        for state in states:
            if not MissionState.query.filter_by(value=state["value"]).first():
                db.session.add(
                    MissionState(name=state["name"], value=state["value"]))
        db.session.commit()
        for state in MissionState.query.all():
            filtered_states = list(
                filter(lambda x: x["prev"] == state.name, states))
            for child_state in filtered_states:
                child = MissionState.query.filter_by(
                    value=child_state.get("value", None)).first()
                if child and child.value not in [x.value for x in state.valid_state_changes]:
                    state.valid_state_changes.append(child)
            db.session.merge(state)
        db.session.commit()
    with open("./src/data/locations.json", "rt") as statefile:
        locations = json.loads(statefile.read())
        for json_location in locations:
            if not Location.query.filter_by(name=json_location["name"]).first():
                db.session.add(Location(
                    name=json_location["name"],
                    description=json_location["description"]
                ))
        db.session.commit()
        for db_location in Location.query.all():
            json_loc = list(
                filter(lambda x: x["name"] == db_location.name, locations))[0]
            parent_name = None
            if db_location.parent:
                parent_name = db_location.parent.name
            db_location.parent = Location.query.filter_by(
                name=json_loc["parent"]).first()
            db.session.merge(db_location)
        db.session.commit()
