
def test_register_success(client):
    res = client.post("/api/v1/auth/register", json={
        "full_name": "David Elroyy",
        "email":     "david@test.com",
        "password":  "secret123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["user"]["email"] == "david@test.com"
    assert "password" not in data["user"]
    assert "password_hash" not in data["user"]

def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "full_name": "David",
        "email":     "duplicate@test.com",
        "password":  "secret123"
    })
    res = client.post("/api/v1/auth/register", json={
        "full_name": "David Again",
        "email":     "duplicate@test.com",
        "password":  "secret123"
    })
    assert res.status_code == 409

def test_register_missing_fields(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "missing@test.com"
    })
    assert res.status_code == 422

def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "full_name": "Login User",
        "email":     "login@test.com",
        "password":  "secret123"
    })
    res = client.post("/api/v1/auth/login", json={
        "email":    "login@test.com",
        "password": "secret123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data

def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "full_name": "Wrong Pass",
        "email":     "wrongpass@test.com",
        "password":  "secret123"
    })
    res = client.post("/api/v1/auth/login", json={
        "email":    "wrongpass@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401

def test_login_nonexistent_email(client):
    res = client.post("/api/v1/auth/login", json={
        "email":    "ghost@test.com",
        "password": "secret123"
    })
    assert res.status_code == 401