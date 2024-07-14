from banks.interface.views.api import VERSION


def test_health_should_return_200_when_aplication_is_alive(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {
        "service": "banks-api",
        "version": VERSION
    }
