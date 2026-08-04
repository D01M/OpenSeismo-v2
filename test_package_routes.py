import pytest

from openseismo.app import create_app
from tsunami_warning import TsunamiWarningSystem


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_tsunami_warning_import():
    assert TsunamiWarningSystem is not None


def test_tsunami_info_endpoint(client):
    response = client.get('/api/tsunami/info')
    assert response.status_code == 200
    payload = response.get_json()
    assert 'warning_levels' in payload


def test_intensity_mmi_endpoint(client):
    response = client.post('/api/intensity/mmi-shindo', json={
        'magnitude': 6.0,
        'depth_km': 20,
        'latitude': 35.0,
        'longitude': 140.0,
        'distance_km': 0.1,
    })
    assert response.status_code == 200
    payload = response.get_json()
    assert 'mmi' in payload and 'shindo' in payload


def test_metadata_endpoint(client):
    response = client.get('/api/volcanoes')
    assert response.status_code == 200
    payload = response.get_json()
    assert 'features' in payload


def test_alert_preferences_endpoint(client):
    response = client.get('/api/alerts/preferences')
    assert response.status_code == 200
    payload = response.get_json()
    assert payload['sound_enabled'] is True
    assert 'alert_levels' in payload
