
def test_dashboard_summary(client, auth_headers):
    res = client.get(
        "/api/v1/dashboard/summary",
        headers=auth_headers
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "total_items"      in data
    assert "total_categories" in data
    assert "low_stock"        in data
    assert "damaged_items"    in data
    assert "pending_returns"  in data

def test_dashboard_requires_auth(client):
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 401