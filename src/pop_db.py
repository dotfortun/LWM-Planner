from app import app
from api.models import (
    db, MissionState, Location, User,
    GearType, Gear, Transaction, Pilot,
    Mission, Setting
)
from api.schemas import MissionSchemas
import json
import random

with app.app_context():
    db_setup_done = Setting.query.filter_by(key="popdb.done").first()
    if not db_setup_done or not db_setup_done.setting:
        gear_types = [
            GearType(name="Frame", value="FRAME"),
            GearType(name="System", value="SYSTEM"),
            GearType(name="Weapon", value="WEAPON"),
            GearType(name="Weapon Mod", value="MOD"),
        ]

        for i in gear_types:
            db.session.add(i)
        db.session.commit()

        gear_types = {
            gt.value: gt for gt in GearType.query.all()
        }

        gear = []

        with open("./src/data/frames.json", "rt") as framefile:
            frames = json.loads(framefile.read())
            for frame in frames[1:]:
                gear.append(Gear(
                    name=' '.join([frame["source"], frame["name"]]),
                    description=frame.get("description", ""),
                    gear_type=gear_types["FRAME"],
                    weight=0.5
                ))
        with open("./src/data/mods.json", "rt") as modfile:
            mods = json.loads(modfile.read())
            for mod in mods[1:]:
                gear.append(Gear(
                    name=' '.join([mod["source"], mod["name"]]),
                    description=mod.get("description", ""),
                    gear_type=gear_types["MOD"],
                    weight=0.5
                ))
        with open("./src/data/systems.json", "rt") as systemfile:
            systems = json.loads(systemfile.read())
            for system in systems[1:]:
                gear.append(Gear(
                    name=' '.join([system["source"], system["name"]]),
                    description=system.get("description", ""),
                    gear_type=gear_types["SYSTEM"],
                    weight=0.5
                ))
        with open("./src/data/weapons.json", "rt") as weaponfile:
            weapons = json.loads(weaponfile.read())
            for weapon in weapons[1:]:
                gear.append(Gear(
                    name=weapon["name"],
                    description=weapon.get("description", ""),
                    gear_type=gear_types["WEAPON"],
                    weight=0.5
                ))

        for i in gear:
            db.session.add(i)
        db.session.commit()

        user = User(
            email="test@test.com",
            password="asdf",
            is_admin=True
        )

        pilot = Pilot(
            name="Test McTestington",
            callsign="Testy",
            hull=1,
            agility=2,
            systems=3,
            engineering=4
        )

        user.pilots.append(pilot)
        db.session.merge(user)

        pilot = Pilot.query.first()

        gear = Gear.query.all()

        for item in random.choices(gear, k=25):
            db.session.add(Transaction(
                item=item,
                pilot=pilot,
                cost=0
            ))
        db.session.commit()

        # Loading MissionStates

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

        # Loading locations

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
        
        with open("./src/data/missions.json", "rt") as missionfile:
            missions = json.loads(missionfile.read())
            for mission in missions:
                m_json = MissionSchemas.MissionIn().load(mission)
                db.session.merge(Mission(**m_json))
            db.session.commit()

        popdb = Setting(
            key="popdb.done",
            setting=True
        )
        db.session.add(popdb)
        db.session.commit()
