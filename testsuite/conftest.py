from pytest import fixture
from meetings.app import create_app
from meetings.models import db


TEST_CONFIG = {
    'SECRET_KEY': 'test',
    'ASSETS_DEBUG': True,
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
}


@fixture
def app(request):
    app = create_app(TEST_CONFIG)
    app_context = app.app_context()
    app_context.push()

    db.create_all()

    @request.addfinalizer
    def fin():
        app_context.pop()

    return app
