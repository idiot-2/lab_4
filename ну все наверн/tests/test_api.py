import pytest
import json


class TestAPIv1Products:
    """Integration tests for API v1 products endpoints."""

    def test_get_products(self, client):
        """Test getting all products via API."""
        response = client.get('/api/v1/products')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data

    def test_create_product_success(self, client):
        """Test creating a product via API."""
        product_data = {
            'name': 'API Test Product',
            'price': 29.99,
            'image': 'test.jpg'
        }
        response = client.post('/api/v1/products',
                              data=json.dumps(product_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'id' in data

    def test_create_product_invalid_input(self, client):
        """Test creating product with invalid input."""
        invalid_data = {'name': 'Test'}  # Missing price
        response = client.post('/api/v1/products',
                              data=json.dumps(invalid_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_get_product_by_id(self, client):
        """Test getting product by ID via API."""
        # First create a product
        product_data = {'name': 'Test Product', 'price': 19.99}
        create_response = client.post('/api/v1/products',
                                     data=json.dumps(product_data),
                                     content_type='application/json')
        product_id = json.loads(create_response.data)['id']

        # Now get it
        response = client.get(f'/api/v1/products/{product_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['product']['name'] == 'Test Product'

    def test_get_product_by_id_not_found(self, client):
        """Test getting nonexistent product."""
        response = client.get('/api/v1/products/99999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestAPIv1Orders:
    """Integration tests for API v1 orders endpoints."""

    def test_get_orders(self, client):
        """Test getting all orders via API."""
        response = client.get('/api/v1/orders')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data

    def test_create_order(self, client):
        """Test creating an order via API."""
        # First create a product
        product_data = {'name': 'Order Test Product', 'price': 15.0}
        create_response = client.post('/api/v1/products',
                                     data=json.dumps(product_data),
                                     content_type='application/json')
        product_id = json.loads(create_response.data)['id']

        order_data = {
            'email': 'order@example.com',
            'address': 'Test Address 123',
            'cart': {
                str(product_id): {
                    'id': product_id,
                    'name': 'Order Test Product',
                    'price': 15.0,
                    'quantity': 2
                }
            }
        }
        response = client.post('/api/v1/orders',
                              data=json.dumps(order_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'

    def test_create_order_invalid_input(self, client):
        """Test creating order with invalid input."""
        invalid_data = {'email': 'test@example.com'}  # Missing address and cart
        response = client.post('/api/v1/orders',
                              data=json.dumps(invalid_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestHealthCheck:
    """Integration test for health check endpoint."""

    def test_health_check_success(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert data['database'] == 'reachable'