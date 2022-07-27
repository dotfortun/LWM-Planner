
import os
from flask_admin import Admin
from .models import (
    db, User, Pilot, Transaction, Gear,
    Mission, Location, MissionState
)
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField, DateTimeField


class UserView(ModelView):
    column_list = ['email', 'is_active', 'pilots']
    column_editable_list = ['is_active', ]
    column_exclude_list = ['_password', ]
    form_extra_fields = {
        'password': PasswordField('password')
    }


class PilotView(ModelView):
    column_list = [
        'name',
        'callsign',
        'manna',
        'mission_history',
    ]


class LocationView(ModelView):
    column_list = [
        'name',
        'description',
        'child_locations',
        'mission_history',
    ]


class MissionView(ModelView):
    column_list = [
        'id',
        'name',
        'gm',
        'description',
        'difficulty',
        'is_job',
        'state',
        'location',
        'loot',
        'pilots',
    ]
    form_extra_fields = {
        'schedule': DateTimeField('schedule')
    }


class MissionStateView(ModelView):
    column_list = [
        'id',
        'value',
        'name',
        'valid_state_changes',
    ]
    column_editable_list = [
        'name',
    ]


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'
    admin = Admin(app, name='LWM Planner Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(PilotView(Pilot, db.session))
    admin.add_view(ModelView(Transaction, db.session))
    admin.add_view(ModelView(Gear, db.session))
    admin.add_view(MissionView(Mission, db.session))
    admin.add_view(MissionStateView(MissionState, db.session))
    admin.add_view(LocationView(Location, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
