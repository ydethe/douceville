import pytest


@pytest.fixture()
def client():
    from douceville.app import app

    app.config["LOGIN_DISABLED"] = True

    return app.test_client()


@pytest.fixture()
def runner():
    from douceville.app import app

    app.config["LOGIN_DISABLED"] = True

    return app.test_cli_runner()
