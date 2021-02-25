import json
import pytest
from flaskr.db import get_db


def test_audio_file_detail_success(client):
    response = client.get('/song/1')
    assert response.status_code == 200
    assert b'name_of_song' in response.data

def test_audio_file_detail_fail(client):
    response = client.get('/song/4')
    assert response.status_code == 400
    assert b'Invalid request' in response.data


def test_audio_file_delete_success(client, app):
    response = client.delete('/song/1')
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM song').fetchone()[0]
        assert count == 1


def test_audio_file_delete_fail(client):
    response = client.delete('/sonjskdg/1')
    assert response.status_code == 400


def test_audio_file_update_success(client):
    data = {
        "audioFileType": "song",
        "audioFileMetadata": {
            "name_of_song": "sdfdddddurew",
            "duration": 876,
            "uploaded_time": "2021-02-25 10:01:33",
        }
    }
    response = client.put('/song/1', data=json.dumps(data))
    assert response.status_code == 200

def test_audio_file_update_fail(client):
    data = {
        "audioFileType": "song",
        "audioFileMetadata": {
            "name_of_song": "sdfdddddurew",
            "duration": "876",
            "uploaded_time": "2021-02-25 10:01:33",
            "id": 3
        }
    }
    response = client.put('/sonjskdg/1', data=json.dumps(data))
    assert response.status_code == 400


def test_audio_file_list_success(client, app):
    response = client.get('song/')
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM song').fetchone()[0]
        assert count == 2


def test_audio_file_list_fail(client):
    response = client.get('songer/')
    assert response.status_code == 400



def test_audio_file_create_success(client, app):
    data = {
        "audioFileType": "song",
        "audioFileMetadata": {
            "name_of_song": "sdfdddddurew",
            "duration": "876",
            "uploaded_time": "2021-02-25 10:01:33",
            "id": 3
        }
    }
    response = client.post('/', data=json.dumps(data))
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM song').fetchone()[0]
        assert count == 3


def test_audio_file_create_fail(client):
    data = {
        "audioFileType": "podcast",
        "audioFileMetadata": {
            "name_of_song": "sdfdddddurew",
            "duration": "876",
            "uploaded_time": "2021-02-25 10:01:33",
        }
    }
    response = client.post('/', data=json.dumps(data))
    assert response.status_code == 400
    