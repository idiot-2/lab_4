import pytest
import json

class TestHomeRoutes:
    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'Головна' in response.get_data(as_text=True)

    def test_about_page(self, client):
        response = client.get('/about')
        assert response.status_code == 200

    def test_api_demo_page(self, client):
        response = client.get('/api-demo')
        assert response.status_code == 200

class TestAuthRoutes:
    def test_register_get(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_register_post_success(self, client):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_register_post_password_mismatch(self, client):
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'password123',
            'confirm_password': 'different'
        }
        response = client.post('/register', data=data)
        assert response.status_code == 200
        assert 'Паролі не співпадають' in response.get_data(as_text=True)

    def test_login_get(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_login_post_success(self, client):
        # First register
        client.post('/register', data={
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        # Then login
        response = client.post('/login', data={
            'identifier': 'loginuser',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_post_wrong_password(self, client):
        response = client.post('/login', data={
            'identifier': 'nonexistent',
            'password': 'wrong'
        })
        assert response.status_code == 200
        assert 'bg-red-900' in response.get_data(as_text=True)

    def test_logout(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

class TestAPIRoutes:
    def test_api_v1_products_get(self, client):
        response = client.get('/api/v1/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data

    def test_api_v1_products_post(self, client):
        data = {'name': 'API Product', 'price': 15.99}
        response = client.post('/api/v1/products', json=data)
        assert response.status_code == 201

    def test_api_v1_products_post_invalid(self, client):
        data = {'price': 10}  # missing name
        response = client.post('/api/v1/products', json=data)
        assert response.status_code == 400

    def test_api_v1_orders_get(self, client):
        response = client.get('/api/v1/orders')
        assert response.status_code == 200

    def test_api_v1_orders_post(self, client):
        data = {
            'email': 'api@example.com',
            'address': 'API Address',
            'cart': {'1': {'id': 1, 'price': 10.00, 'quantity': 1}}
        }
        response = client.post('/api/v1/orders', json=data)
        assert response.status_code == 201

    def test_api_v1_orders_post_invalid(self, client):
        data = {'email': 'test@example.com'}  # missing address and cart
        response = client.post('/api/v1/orders', json=data)
        assert response.status_code == 400

    def test_api_v2_products_get(self, client):
        response = client.get('/api/v2/products')
        assert response.status_code == 200

    def test_api_v2_orders_get(self, client):
        response = client.get('/api/v2/orders')
        assert response.status_code == 200

class TestFeedbackRoutes:
    def test_feedback_get(self, client):
        response = client.get('/feedback')
        assert response.status_code == 200

    def test_feedback_post(self, client):
        data = {
            'name': 'Test User',
            'email': 'feedback@example.com',
            'message': 'Test message'
        }
        response = client.post('/feedback', data=data)
        assert response.status_code == 200
        assert b'success' in response.data

class TestHealthCheck:
    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'