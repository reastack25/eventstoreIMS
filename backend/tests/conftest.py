# tests/conftest.py

import pytest
import uuid
from app import create_app
from extensions import db as _db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING":        True,
        "JWT_SECRET_KEY": "test-secret-key-that-is-long-enough-32chars",
        "SECRET_KEY":     "test-secret-key-that-is-long-enough-32chars",
    })
    return app

@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.create_all()   # create all tables before tests run
        yield _db
        _db.session.remove()
        _db.drop_all()     # clean up after all tests finish

@pytest.fixture(scope="function")
def client(app, db):
    with app.test_client() as client:
        with app.app_context():
            yield client
            _db.session.rollback()  # rollback after each test

@pytest.fixture(scope="function")
def auth_headers(client, app):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@elroyy.com"

    with app.app_context():
        client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email":     unique_email,
            "password":  "secret123"
        })

        response = client.post("/api/v1/auth/login", json={
            "email":    unique_email,
            "password": "secret123"
        })

    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def seeded_item(app, db):
    from models.category import Category
    from models.item import Item

    with app.app_context():
        unique_name = f"Test Category {uuid.uuid4().hex[:8]}"
        unique_code = f"TST-{uuid.uuid4().hex[:6].upper()}"

        category = Category(name=unique_name, description="Test")
        _db.session.add(category)
        _db.session.flush()

        item = Item(
            code        = unique_code,
            name        = f"Test Item {uuid.uuid4().hex[:6]}",
            category_id = category.id,
            unit        = "piece",
            quantity    = 0,
            available   = 0,
            status      = "ACTIVE"
        )
        _db.session.add(item)
        _db.session.commit()

        return item.id