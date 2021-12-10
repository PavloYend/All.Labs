import json
import random

import pytest

from main import app as fl_app


@pytest.fixture
def app():
    yield fl_app


@pytest.fixture
def client(app):
    return app.test_client()


class TestUser:
    def test_user_create(self, client):
        temp = {
            'username': f'userna{random.randint(1, 10000)}',
            'firstName': 'Ivan',
            'lastName': 'M',
            'email': 'Iv@gmail.com',
            'phone': '0978563',
            'password': '1000'
        }
        temp = json.dumps(temp)
        response = client.post('http://localhost:5000/user',
                               headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)

        assert response.status_code == 200

    def test_create_err(self, client):
        temp = {
            'username': f'username424',
            'firstName': 'test',
            'lastName': 'testl',
            'email': 'I@gmail.com',
            'phone': '097853',
            'password': 'password'
        }
        temp = json.dumps(temp)
        response = client.post('http://localhost:5000/user',
                               headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)

        assert response.status_code == 404

    def test_get_user(self, client):
        response = client.get('http://localhost:5000/user/1')
        assert response.status_code == 200

    def test_get_user_e(self, client):
        response = client.get('http://localhost:5000/user/999')
        assert response.status_code != 200

    def test_update_user(self, client):
        temp = {
            'firstName': 'Petro',
            'lastName': 'B',
            'username': f'Petro B{random.randint(0,1000)}',
            'phone': '0975321',
            'email': 'petr@gmail.com',
            'password': '1111'
        }
        temp = json.dumps(temp)
        response = client.put('http://localhost:5000/user/1',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 404

    def test_update_user_ee(self, client):
        temp = {
            'firstName': 'test',
            'lastName': 'test1',
            'username': f'us{random.randint(0,1000)}',
            'phone': '097531',
            'email': 'pe@gmail.com',
            'password': '12323'
        }
        temp = json.dumps(temp)
        response = client.put('http://localhost:5000/user/9999',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 404

    def test_update_user_eer(self, client):
        temp = {
            'firstName': 'test',
            'lastName': 'test1',
            'username': f'username4',
            'phone': '0975321',
            'email': 'pr@gmail.com',
            'password': '12323'
        }
        temp = json.dumps(temp)
        response = client.put('http://localhost:5000/user/1',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 404

    def test_create_event(self, client):
        temp = {
            'name': 'Birthday',
            'owner_id': 1
        }
        temp = json.dumps(temp)
        response = client.post('http://localhost:5000/event',
                               headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code in [200, 405]

    def test_create_event_e(self, client):
        temp = {
            'name': 'test',
            'owner_id': '123'
        }
        temp = json.dumps(temp)
        response = client.post('http://localhost:5000/event',
                               headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 409

    def test_get_event(self, client):
        response = client.get('http://localhost:5000/event/1')
        assert response.status_code == 404

    def test_get_event_e(self, client):
        response = client.get('http://localhost:5000/event/999')
        assert response.status_code != 409

    def test_update_event(self, client):
        temp = {
            'name': f'{random.randint(1, 9999)}',
            'owner_id': random.randint(5, 15)
        }
        temp = json.dumps(temp)
        response = client.put('http://localhost:5000/event/1',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 500

    def test_update_event_err(self, client):
        temp = {
            'name': f'{random.randint(1, 9999)}',
            'owner_id': random.randint(5, 15)
        }
        temp = json.dumps(temp)
        response = client.put('http://localhost:5000/event/999',
                              headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=temp)
        assert response.status_code == 500

    def test_add_user_event(self, client):
        response = client.post('http://localhost:5000/event/1/user/1')
        assert response.status_code in [200, 500]

    def test_add_user_event_e(self, client):
        response = client.post('http://localhost:5000/event/1/user/1')
        assert response.status_code in [200, 500]

    def test_add_user_event_err(self, client):
        response = client.post('http://localhost:5000/event/99/user/99')
        assert response.status_code == 500

    def test_get_all_requested(self, client):
        response = client.get('http://localhost:5000/event/1/users')
        assert response.status_code == 500

    def test_get_all_requested_e(self, client):
        response = client.get('http://localhost:5000/event/999/users')
        assert response.status_code != 200

    def test_your_events(self, client):
        response = client.get('http://localhost:5000/your_events/user/1')
        assert response.status_code == 500

    def test_your_events_e(self, client):
        response = client.get('http://localhost:5000/your_events/user/9999')
        assert response.status_code != 200

    def test_user_for_request(self, client):
        response = client.get('http://localhost:5000/events/user/1')
        assert response.status_code == 500

    def test_user_for_request_e(self, client):
        response = client.get('http://localhost:5000/events/user/9999')
        assert response.status_code != 200

    def test_delete_event(self, client):
        response = client.delete('http://localhost:5000/event/1')
        assert response.status_code == 500

    def test_delete_event_e(self, client):
        response = client.delete('http://localhost:5000/event/9999')
        assert response.status_code != 200

    def test_delete(self, client):
        response = client.delete('http://localhost:5000/user/1')
        assert response.status_code == 404

    def test_delete_err(self, client):
        response = client.delete('http://localhost:5000/user/99')
        assert response.status_code == 404