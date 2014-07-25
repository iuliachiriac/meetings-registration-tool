from wtforms import Form
from wtforms import StringField, PasswordField, validators
from flask.ext.login import current_user

from uuid import uuid4
from datetime import datetime

from .base import BaseForm
from mrt.models import db, User


class LoginForm(Form):

    email = StringField('Email')
    password = PasswordField('Password')

    def validate_email(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')

        if not user.is_active:
            raise validators.ValidationError('Inactive user')

    def validate_password(self, field):
        user = self.get_user()
        if user and not user.check_password(self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(email=self.email.data).first()


class UserForm(BaseForm):

    class Meta:
        model = User


class RecoverForm(Form):

    email = StringField('Email', [validators.DataRequired()])

    def validate_email(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')

    def get_user(self):
        return User.query.filter_by(email=self.email.data).first()

    def save(self):
        user = self.get_user()
        token = str(uuid4())
        time = datetime.now()

        user.recover_token = token
        user.recover_time = time
        db.session.commit()

        return user


class ResetPasswordForm(Form):

    password = PasswordField('Password', [validators.DataRequired()])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

    def validate_confirm(self, field):
        if self.password.data != self.confirm.data:
            raise validators.ValidationError('Passwords differ!')


class ChangePasswordForm(Form):
    password = PasswordField('Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired()])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

    def validate_password(self, field):
        if not current_user.check_password(self.password.data):
            raise validators.ValidationError('Password is incorrect')

    def validate_confirm(self, field):
        if self.new_password.data != self.confirm.data:
            raise validators.ValidationError('Passwords differ')

    def save(self):
        user = current_user
        user.set_password(self.new_password.data)
        db.session.commit()

        return user
