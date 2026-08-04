from openseismo import config


def test_flask_host_allows_localhost_access():
    assert config.FLASK_HOST == "0.0.0.0"
