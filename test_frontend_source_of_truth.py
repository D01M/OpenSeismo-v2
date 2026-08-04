from pathlib import Path

from server import app


def test_frontend_serves_only_openseismo_assets():
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    body = response.get_data(as_text=True)

    assert 'ACTIVE UI: v2' in body
    assert str(Path('openseismo/templates').resolve()) in app.template_folder
    assert str(Path('openseismo/static').resolve()) in app.static_folder

    css_response = client.get('/static/css/base.css')
    assert css_response.status_code == 200
