from functools import wraps
from flask.views import MethodView
from flask import g, render_template, request, session, abort
from flask import redirect, url_for
from flask.ext.login import login_user, current_user

from mrt.models import Participant, db
from mrt.forms.meetings import custom_form_factory
from mrt.forms.meetings import RegistrationForm, RegistrationUserForm
from mrt.forms.auth import LoginForm
from mrt.signals import activity_signal, notification_signal
from mrt.signals import registration_signal


def _render_if_closed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.meeting.online_registration:
            return render_template('meetings/registration/closed.html')
        return func(*args, **kwargs)
    return wrapper


class Registration(MethodView):

    decorators = (_render_if_closed,)

    def get(self):
        Form = custom_form_factory(registration_fields=True,
                                   form=RegistrationForm)
        form = Form()
        if current_user.is_authenticated():
            participant = current_user.participants.filter_by(
                meeting=None,
                category=None).first()
            form = Form(obj=participant)
        return render_template('meetings/registration/form.html',
                               form=form)

    def post(self):
        Form = custom_form_factory(registration_fields=True,
                                   form=RegistrationForm)
        form = Form(request.form)
        if form.validate():
            participant = form.save()
            activity_signal.send(self, participant=participant,
                                 action='add')
            notification_signal.send(self, participant=participant)
            registration_signal.send(self, participant=participant)

            user_form = RegistrationUserForm(email=participant.email)
            session['registration_token'] = participant.registration_token

            return render_template('meetings/registration/success.html',
                                   participant=participant,
                                   form=user_form)
        return render_template('meetings/registration/form.html',
                               form=form)


class UserRegistration(MethodView):

    def post(self):
        registration_token = session.get('registration_token', None)
        if not registration_token:
            abort(400)
        participant = Participant.query.filter_by(
            registration_token=registration_token).first_or_404()

        form = RegistrationUserForm(request.form)
        if form.validate():
            session.pop('registration_token', None)
            participant.user = form.save()
            db.session.flush()
            default_participant = participant.clone()
            db.session.add(default_participant)
            db.session.commit()
        return render_template('meetings/registration/user_success.html',
                               participant=participant,
                               form=form)


class UserRegistrationLogin(MethodView):

    def get(self):
        form = LoginForm()
        return render_template('meetings/registration/user_login.html',
                               form=form)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            user = form.get_user()
            login_user(user)
            return redirect(url_for('meetings.registration'))
        return render_template('meetings/registration/user_login.html',
                               form=form)
