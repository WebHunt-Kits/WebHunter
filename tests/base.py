import os

import pytest

from flask_mico.app import create_app

os.environ.setdefault('FLASKMICO_SETTINGS_MODULE', 'conf.development.settings')
application = create_app()

@pytest.fixture
def client():
    with application.test_client() as client:
        yield client
