import pytest
from models import (
    get_products, get_product_by_id, create_product, update_product, delete_product,
    create_user, verify_user, get_user_by_username, get_user_by_email,
    add_order, get_orders, get_order_details, update_order_status, delete_order
)

class TestProductModel:
    def test_get_products_empty(self):
        products = get_products()
        assert products == []

    def test_create_product(self):
        product_id = create_product("Test Product", 10.99, "test.jpg")
        assert product_id is not None
        assert isinstance(product_id, int)

    def test_get_products_after_create(self):
        create_product("Product 1", 15.00)
        create_product("Product 2", 20.00)
        products = get_products()
        assert len(products) == 2
        assert products[0]['name'] == "Product 1"
        assert products[1]['price'] == 20.00

    def test_get_product_by_id(self):
        product_id = create_product("Unique Product", 25.00)
        product = get_product_by_id(product_id)
        assert product is not None
        assert product['name'] == "Unique Product"
        assert product['price'] == 25.00

    def test_get_product_by_id_not_found(self):
        product = get_product_by_id(999)
        assert product is None

    def test_update_product(self):
        product_id = create_product("Old Name", 10.00)
        success = update_product(product_id, name="New Name", price=15.00)
        assert success
        product = get_product_by_id(product_id)
        assert product['name'] == "New Name"
        assert product['price'] == 15.00

    def test_update_product_not_found(self):
        success = update_product(999, name="Test")
        assert not success

    def test_delete_product(self):
        product_id = create_product("To Delete", 5.00)
        success = delete_product(product_id)
        assert success
        product = get_product_by_id(product_id)
        assert product is None

    def test_delete_product_not_found(self):
        success = delete_product(999)
        assert not success

class TestUserModel:
    def test_create_user(self):
        user_id = create_user("testuser", "test@example.com", "password123")
        assert user_id != 0

    def test_create_user_duplicate_username(self):
        create_user("user1", "email1@example.com", "pass")
        user_id = create_user("user1", "email2@example.com", "pass")
        assert user_id == 0  # Assuming 0 means failure

    def test_verify_user_correct(self):
        create_user("verifyuser", "verify@example.com", "correctpass")
        user = verify_user("verifyuser", "correctpass")
        assert user is not None
        assert user['username'] == "verifyuser"

    def test_verify_user_wrong_password(self):
        create_user("wrongpass", "wrong@example.com", "rightpass")
        user = verify_user("wrongpass", "wrongpass")
        assert user is None

    def test_verify_user_not_found(self):
        user = verify_user("nonexistent", "password")
        assert user is None

    def test_get_user_by_username(self):
        create_user("getuser", "get@example.com", "pass")
        user = get_user_by_username("getuser")
        assert user is not None
        assert user['email'] == "get@example.com"

    def test_get_user_by_email(self):
        create_user("emailuser", "emailtest@example.com", "pass")
        user = get_user_by_email("emailtest@example.com")
        assert user is not None
        assert user['username'] == "emailuser"

class TestOrderModel:
    def test_add_order(self):
        cart = {
            '1': {'id': 1, 'price': 10.00, 'quantity': 2},
            '2': {'id': 2, 'price': 5.00, 'quantity': 1}
        }
        # First create products
        create_product("Prod1", 10.00)
        create_product("Prod2", 5.00)
        add_order("order@example.com", "Test Address", cart)
        orders = get_orders()
        assert len(orders) >= 1

    def test_get_orders(self):
        orders = get_orders()
        assert isinstance(orders, list)

    def test_get_order_details(self):
        cart = {'1': {'id': 1, 'price': 10.00, 'quantity': 1}}
        create_product("Prod", 10.00)
        add_order("details@example.com", "Addr", cart)
        order_id = get_orders()[-1]['id']  # Get last order
        order, items = get_order_details(order_id)
        assert order is not None
        assert len(items) == 1

    def test_update_order_status(self):
        cart = {'1': {'id': 1, 'price': 10.00, 'quantity': 1}}
        create_product("Prod", 10.00)
        add_order("status@example.com", "Addr", cart)
        order_id = get_orders()[-1]['id']
        update_order_status(order_id, "Shipped")
        order, _ = get_order_details(order_id)
        assert order['status'] == "Shipped"

    def test_delete_order(self):
        cart = {'1': {'id': 1, 'price': 10.00, 'quantity': 1}}
        create_product("Prod", 10.00)
        add_order("delete@example.com", "Addr", cart)
        orders_before = len(get_orders())
        order_id = get_orders()[-1]['id']
        delete_order(order_id)
        orders_after = len(get_orders())
        assert orders_after == orders_before - 1