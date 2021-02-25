import json
import pytest
from flaskr.db import get_db


def test_audio_file_detail_success(client):
    response = client.get('/song/1')
    assert response.status_code == 200

def test_audio_file_detail_fail(client):
    response = client.get('/song/4')
    assert response.status_code == 400


def test_audio_file_delete_success(client):
    response = client.delete('/song/1')
    assert response.status_code == 200

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


def test_audio_file_list_success(client):
    response = client.get('song/')
    assert response.status_code == 200


def test_audio_file_list_fail(client):
    response = client.get('songer/')
    assert response.status_code == 400



def test_audio_file_create_success(client):
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
    