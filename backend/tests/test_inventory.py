
def test_receive_stock(client, auth_headers, seeded_item):
    res = client.post("/api/v1/inventory/receive",
        json={
            "item_id":  seeded_item,
            "quantity": 50,
            "remarks":  "Initial stock"
        },
        headers=auth_headers
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["item"]["quantity"]  == 50
    assert data["item"]["available"] == 50

def test_receive_requires_auth(client, seeded_item):
    res = client.post("/api/v1/inventory/receive", json={
        "item_id":  seeded_item,
        "quantity": 10
    })
    assert res.status_code == 401

def test_receive_invalid_quantity(client, auth_headers, seeded_item):
    res = client.post("/api/v1/inventory/receive",
        json={"item_id": seeded_item, "quantity": -5},
        headers=auth_headers
    )
    assert res.status_code == 422

def test_dispatch_stock(client, auth_headers, seeded_item):
    # First receive stock
    client.post("/api/v1/inventory/receive",
        json={"item_id": seeded_item, "quantity": 50},
        headers=auth_headers
    )
    res = client.post("/api/v1/inventory/dispatch",
        json={
            "item_id":  seeded_item,
            "quantity": 10,
            "job_card": "JC-001"
        },
        headers=auth_headers
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["item"]["available"] == 40  # 50 - 10
    assert data["item"]["quantity"]  == 50  # unchanged

def test_dispatch_insufficient_stock(client, auth_headers, seeded_item):
    res = client.post("/api/v1/inventory/dispatch",
        json={
            "item_id":  seeded_item,
            "quantity": 9999,
            "job_card": "JC-002"
        },
        headers=auth_headers
    )
    assert res.status_code == 409

def test_return_stock(client, auth_headers, seeded_item):
    # Receive then dispatch first
    client.post("/api/v1/inventory/receive",
        json={"item_id": seeded_item, "quantity": 50},
        headers=auth_headers
    )
    client.post("/api/v1/inventory/dispatch",
        json={"item_id": seeded_item, "quantity": 10, "job_card": "JC-001"},
        headers=auth_headers
    )
    res = client.post("/api/v1/inventory/return",
        json={
            "item_id":  seeded_item,
            "quantity": 5,
            "job_card": "JC-001"
        },
        headers=auth_headers
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["item"]["available"] == 45  # 50 - 10 + 5

def test_damage_stock(client, auth_headers, seeded_item):
    # Receive first
    client.post("/api/v1/inventory/receive",
        json={"item_id": seeded_item, "quantity": 50},
        headers=auth_headers
    )
    res = client.post("/api/v1/inventory/damage",
        json={
            "item_id":  seeded_item,
            "quantity": 2,
            "reason":   "Broken during transport"
        },
        headers=auth_headers
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["item"]["quantity"]  == 48  # 50 - 2
    assert data["item"]["available"] == 48  # 50 - 2

def test_damage_exceeds_available(client, auth_headers, seeded_item):
    res = client.post("/api/v1/inventory/damage",
        json={
            "item_id":  seeded_item,
            "quantity": 9999,
            "reason":   "Test"
        },
        headers=auth_headers
    )
    assert res.status_code == 409