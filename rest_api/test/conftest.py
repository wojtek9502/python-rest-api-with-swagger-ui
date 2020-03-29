# This is file with fixtures for tests
# fixtures from file named conftest.py will be automaticaly import for every test_* file
import pytest
from rest_api.app import app, db


# scope=module means, use this same fixture (one instance created) for all tests in module.
# default scope is function, means every test function have own instance of fixture
@pytest.yield_fixture(scope='function')
def init_new_db_for_every_test():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_for_tests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()
        connection = db.engine.connect()
        session = db.create_scoped_session()

        yield db

        db.session.rollback()
        session.remove()
        connection.close()
        db.drop_all()


@pytest.yield_fixture(scope='module')
def init_db_for_module():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_for_tests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()
        connection = db.engine.connect()
        session = db.create_scoped_session()

        yield db

        session.remove()
        connection.close()
