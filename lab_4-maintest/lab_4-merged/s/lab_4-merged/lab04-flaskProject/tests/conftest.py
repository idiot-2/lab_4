import pytest
import os
import tempfile

# Set TESTING before importing app to prevent seeding
os.environ['TESTING'] = '1'

from app import app as flask_app
from models import init_db, get_products

@pytest.fixture(scope='function', autouse=True)
def setup_test_db():
    db_fd, db_path = tempfile.mkstemp()
    os.environ['DATABASE'] = db_path
    init_db()
    yield
    os.close(db_fd)
    os.unlink(db_path)
    if 'DATABASE' in os.environ:
        del os.environ['DATABASE']

@pytest.fixture
def app():
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    os.environ['DATABASE'] = db_path
    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        init_db()
        # Only seed if not testing
        if not flask_app.config.get('TESTING') and not get_products():
            from seed_data import seed_products
            seed_products()

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)
    if 'DATABASE' in os.environ:
        del os.environ['DATABASE']

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()