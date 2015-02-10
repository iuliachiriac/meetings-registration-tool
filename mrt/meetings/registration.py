from functools import wraps
from flask.views import MethodView
from flask import g, render_template, request, session, abort
from flask import redirect, url_for
from flask.ext.login import login_user, logout_user, current_user

from mrt.forms.auth import LoginForm
from mrt.forms.meetings import custom_form_factory, custom_object_factory
from mrt.forms.meetings import RegistrationForm, RegistrationUserForm
from mrt.forms.meetings import MediaRegistrationForm
from mrt.models import Participant, db, Phrase

from mrt.signals import activity_signal, notification_signal
from mrt.signals import registration_signal
from mrt.utils import set_language, clean_email


def _render_if_closed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.meeting.online_registration:
            return render_template('meetings/registration/closed.html')
        return func(*args, **kwargs)
    return wrapper


def _render_if_media_disabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.meeting.media_participant_enabled:
            abort(404)
        return func(*args, **kwargs)
    return wrapper


class BaseRegistration(MethodView):

    def get_default_participant(self, user):
        raise NotImplementedError

    def get_success_phrase(self):
        raise NotImplementedError

    def get(self):
        lang = request.args.get('lang', 'en')
        if lang in ('en', 'fr', 'es'):
            set_language(lang)
        Form = custom_form_factory(self.form_class, registration_fields=True)
        form = Form()
        if current_user.is_authenticated():
            participant = self.get_default_participant(current_user)
            Object = custom_object_factory(participant)
            form = Form(obj=Object())
        return render_template('meetings/registration/form.html',
                               form=form)

    def post(self):
        Form = custom_form_factory(self.form_class, registration_fields=True)
        form = Form(request.form)
        if form.validate():
            participant = form.save()
            if current_user.is_authenticated():
                participant.user = current_user
                default_participant = self.get_default_participant(
                    current_user)
                if default_participant:
                    default_participant.update(participant)
                else:
                    participant.clone()
            db.session.commit()

            activity_signal.send(self, participant=participant,
                                 action='add')
            notification_signal.send(self, participant=participant)
            registration_signal.send(self, participant=participant)

            email = clean_email(participant.email)
            user_form = RegistrationUserForm(email=email)
            session['registration_token'] = participant.registration_token
            success_phrase = self.get_success_phrase()

            return render_template('meetings/registration/success.html',
                                   participant=participant,
                                   form=user_form,
                                   success_phrase=success_phrase)
        return render_template('meetings/registration/form.html',
                               form=form)


class Registration(BaseRegistration):

    decorators = (_render_if_closed,)
    form_class = RegistrationForm

    def get_default_participant(self, user):
        return user.get_default(Participant.DEFAULT)

    def get_success_phrase(self):
        return g.meeting.phrases.filter_by(group=Phrase.ONLINE_CONFIRMATION,
                                           name=Phrase.PARTICIPANT).scalar()


class MediaRegistration(BaseRegistration):

    decorators = (_render_if_closed, _render_if_media_disabled)
    form_class = MediaRegistrationForm

    def get_default_participant(self, user):
        return user.get_default(Participant.DEFAULT_MEDIA)

    def get_success_phrase(self):
        return g.meeting.phrases.filter_by(group=Phrase.ONLINE_CONFIRMATION,
                                           name=Phrase.MEDIA).scalar()


class UserRegistration(MethodView):

    def post(self):
        if current_user.is_authenticated():
            abort(404)
        registration_token = session.get('registration_token', None)
        if not registration_token:
            abort(400)
        participant = (
            Participant.query
            .filter_by(registration_token=registration_token)
            .first_or_404())

        form = RegistrationUserForm(request.form)
        if form.validate():
            session.pop('registration_token', None)
            participant.user = form.save()
            db.session.flush()
            participant.clone()
            db.session.commit()
            return render_template('meetings/registration/user_success.html')
        success_phrase = self.get_success_phrase()
        return render_template('meetings/registration/success.html',
                               participant=participant,
                               success_phrase=success_phrase,
                               form=form)

    def get_success_phrase(self):
        return g.meeting.phrases.filter_by(group=Phrase.ONLINE_CONFIRMATION,
                                           name=Phrase.MEDIA).scalar()


class UserRegistrationLogin(MethodView):

    def get(self):
        form = LoginForm()
        next = request.values.get('next')
        return render_template('meetings/registration/user_login.html',
                               form=form, next=next)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            user = form.get_user()
            login_user(user)
            next = request.values.get('next')
            return redirect(next or url_for('meetings.registration'))
        return render_template('meetings/registration/user_login.html',
                               form=form)


class UserRegistrationLogout(MethodView):

    def get(self):
        logout_user()
        return redirect(url_for('.registration'))
