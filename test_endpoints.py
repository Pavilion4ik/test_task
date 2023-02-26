import dataclasses
import json
from datetime import date
import pytest as pytest
from unittest.mock import patch

from app import app


@dataclasses.dataclass
class Event:
    date: date
    value: int


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_pk(client):
    response = client.get('/api/info')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'possible_filtering' in data


def test_get_timeline(client):
    with patch('app.session') as mock_session:
        mock_events = [
            Event(date=date(2019, 1, 1), value=16),
            Event(date=date(2019, 1, 3), value=15),
        ]
        mock_session.query().filter().all.return_value = mock_events

        response = client.get(
            '/api/timeline?startDate=2019-01-01&endDate=2019-01-03&'
            'Type=cumulative&Grouping=weekly&attr1=value1&attr2=value2')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'timeline' in data
        assert len(data['timeline']) == 2
        assert data['timeline'][0]['date'] == '2019-01-01'
        assert data['timeline'][0]['value'] == 1
        assert data['timeline'][0]['type'] == 'cumulative'
        assert data['timeline'][0]['grouping'] == 'weekly'
        assert data['timeline'][1]['date'] == '2019-01-03'
        assert data['timeline'][1]['value'] == 1
        assert data['timeline'][1]['type'] == 'cumulative'
        assert data['timeline'][1]['grouping'] == 'weekly'

    response = client.get('/api/timeline?startDate=2019-01-01&endDate=2019-01-03&type=invalid&grouping=weekly')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'message' in data
