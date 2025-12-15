import pytest
import os
import tempfile
import uuid
import sqlite3


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Set up a unique test database for each test."""
    # Create a unique temporary database file for each test
    db_fd, db_path = tempfile.mkstemp(suffix=f'_{uuid.uuid4().hex}.db')

    # Import models and patch the connection function
    import models
    original_get_db_connection = models.get_db_connection

    def test_get_db_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    models.get_db_connection = test_get_db_connection

    # Initialize the test database
    models.init_db()

    yield

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    models.get_db_connection = original_get_db_connection


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    from app import app as flask_app
    return flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()