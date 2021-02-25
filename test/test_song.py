import pytest
from flaskr.db import get_db


def test_audio_list(client):
    response = client.get('/')
    print(response)
    