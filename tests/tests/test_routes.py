import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to BLE Scanner" in response.data

def test_scan(client, mocker):
    """Test the scan route"""
    mock_devices = [
        {"name": "Device1", "address": "00:11:22:33:44:55"},
        {"name": "Device2", "address": "66:77:88:99:AA:BB"}
    ]

    mocker.patch('app.routes.scan_ble', return_value=mock_devices)

    response = client.get('/scan')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert json_data[0]['name'] == 'Device1'
    assert json_data[1]['address'] == '66:77:88:99:AA:BB'
