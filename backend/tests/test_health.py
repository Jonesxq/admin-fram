from fastapi.testclient import TestClient


def test_health_returns_standard_response(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["message"] == "ok"
    assert response.json()["data"] == {"status": "ok"}
    assert "request_id" in response.json()
