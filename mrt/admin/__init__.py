from .staff import *
from .category import *
from .phrase import *
from .role import *


from flask import render_template
from flask.views import MethodView


class SettingsOverview(MethodView):

    def get(self):
        return render_template('admin/settings_overview.html')
