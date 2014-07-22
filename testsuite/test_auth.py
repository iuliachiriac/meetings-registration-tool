from flask import url_for

from mrt.models import User
from .factories import UserFactory


def test_login_required_view(app):
    client = app.test_client()
    with app.test_request_context():
        url = url_for('admin.staff')
        resp = client.get(url)

    assert resp.status_code == 302


def test_login_succesfull(app):
    UserFactory()
    data = UserFactory.attributes()

    client = app.test_client()
    with app.test_request_context():
        url = url_for('auth.login')
        resp = client.post(url, data=data)

    assert resp.status_code == 302


def test_recover_password(app):
    user = UserFactory()
    data = UserFactory.attributes()

    client = app.test_client()
    with app.test_request_context():
        url = url_for('auth.recover')
        resp = client.post(url, data=data)

    assert resp.status_code == 302
    user = User.query.get(user.id)
    assert user is not None

    data['confirm'] = data['password'] = 'webdeeau'
    with app.test_request_context():
        url = url_for('auth.reset', token=user.recover_token)
        resp = client.post(url, data=data)

    assert user.check_password('webdeeau')