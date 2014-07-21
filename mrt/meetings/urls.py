from flask import Blueprint
from mrt.meetings import Meetings, MeetingEdit


meetings = Blueprint('meetings', __name__, url_prefix='/meetings')


meetings.add_url_rule('/', view_func=Meetings.as_view('home'))

meeting_edit_func = MeetingEdit.as_view('edit')
meetings.add_url_rule('/add', view_func=meeting_edit_func)
meetings.add_url_rule('/<int:meeting_id>/edit', view_func=meeting_edit_func)
