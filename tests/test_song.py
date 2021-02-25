import pytest
from flaskr.db import get_db


def test_audio_list(client):
    assert client.get('/song').status_code == 200
    