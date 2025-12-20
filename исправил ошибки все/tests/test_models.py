import pytest
from models import (
    create_user, verify_user, get_user_by_username, get_user_by_email,
    get_products, get_product_by_id, create_product, update_product, delete_product,
    add_order, get_orders, get_order_details, update_order_status, delete_order,
    create_promo_code, get_promo_code, get_all_promo_codes, update_promo_code_status,
    delete_promo_code, apply_promo_discount
)


class TestUserFunctions:
    """Unit tests for user-related functions."""

    def test_create_user_success(self):
        """Test successful user creation."""
        user_id = create_user("testuser_unique_1", "test_unique_1@example.com", "password123")
        assert user_id > 0

    def test_create_user_duplicate_username(self):
        """Test creating user with existing username fails."""
        create_user("testuser_unique_2", "test_unique_2@example.com", "password123")
        user_id = create_user("testuser_unique_2", "test_unique_3@example.com", "password123")
        assert user_id == 0

    def test_create_user_duplicate_email(self):
        """Test creating user with existing email fails."""
        create_user("testuser_unique_4", "test_unique_4@example.com", "password123")
        user_id = create_user("testuser_unique_5", "test_unique_4@example.com", "password123")
        assert user_id == 0

    def test_verify_user_correct_credentials(self):
        """Test verifying user with correct credentials."""
        create_user("testuser_unique_6", "test_unique_6@example.com", "password123")
        user = verify_user("testuser_unique_6", "password123")
        assert user is not None
        assert user['username'] == "testuser_unique_6"

    def test_verify_user_wrong_password(self):
        """Test verifying user with wrong password."""
        create_user("testuser_unique_7", "test_unique_7@example.com", "password123")
        user = verify_user("testuser_unique_7", "wrongpassword")
        assert user is None

    def test_verify_user_nonexistent_user(self):
        """Test verifying nonexistent user."""
        user = verify_user("nonexistent_unique", "password123")
        assert user is None

    def test_get_user_by_username(self):
        """Test getting user by username."""
        create_user("testuser_unique_8", "test_unique_8@example.com", "password123")
        user = get_user_by_username("testuser_unique_8")
        assert user is not None
        assert user['email'] == "test_unique_8@example.com"

    def test_get_user_by_email(self):
        """Test getting user by email."""
        create_user("testuser_unique_9", "test_unique_9@example.com", "password123")
        user = get_user_by_email("test_unique_9@example.com")
        assert user is not None
        assert user['username'] == "testuser_unique_9"


class TestProductFunctions:
    """Unit tests for product-related functions."""

    def test_create_product(self):
        """Test creating a product."""
        product_id = create_product("Test Product", 99.99, "test.jpg")
        assert product_id > 0

    def test_get_products(self):
        """Test getting all products."""
        create_product("Product 1", 10.0)
        create_product("Product 2", 20.0)
        products = get_products()
        assert len(products) >= 2
        assert any(p['name'] == "Product 1" for p in products)

    def test_get_product_by_id(self):
        """Test getting product by ID."""
        product_id = create_product("Specific Product", 50.0)
        product = get_product_by_id(product_id)
        assert product is not None
        assert product['name'] == "Specific Product"

    def test_get_product_by_id_not_found(self):
        """Test getting nonexistent product."""
        product = get_product_by_id(99999)
        assert product is None

    def test_update_product(self):
        """Test updating a product."""
        product_id = create_product("Old Name", 100.0)
        success = update_product(product_id, name="New Name", price=150.0)
        assert success
        product = get_product_by_id(product_id)
        assert product['name'] == "New Name"
        assert product['price'] == 150.0

    def test_update_product_not_found(self):
        """Test updating nonexistent product."""
        success = update_product(99999, name="New Name")
        assert not success

    def test_delete_product(self):
        """Test deleting a product."""
        product_id = create_product("To Delete", 75.0)
        success = delete_product(product_id)
        assert success
        product = get_product_by_id(product_id)
        assert product is None

    def test_delete_product_not_found(self):
        """Test deleting nonexistent product."""
        success = delete_product(99999)
        assert not success


class TestOrderFunctions:
    """Unit tests for order-related functions."""

    def test_add_order(self):
        """Test adding an order."""
        # Create a product first
        from models import create_product
        product_id = create_product("Order Test Product", 10.0)
        cart = {str(product_id): {'id': product_id, 'name': 'Order Test Product', 'price': 10.0, 'quantity': 2}}
        add_order("test@example.com", "Test Address", cart)
        orders = get_orders()
        assert len(orders) >= 1

    def test_get_order_details(self):
        """Test getting order details."""
        # Create a product first
        from models import create_product
        product_id = create_product("Test Product", 10.0)
        cart = {str(product_id): {'id': product_id, 'name': 'Test Product', 'price': 10.0, 'quantity': 1}}
        add_order("details@example.com", "Address", cart)
        orders = get_orders()
        if orders:
            order_id = orders[-1]['id']
            order, items = get_order_details(order_id)
            assert order is not None
            assert len(items) > 0

    def test_update_order_status(self):
        """Test updating order status."""
        # Create a product first
        from models import create_product
        product_id = create_product("Status Test Product", 10.0)
        cart = {str(product_id): {'id': product_id, 'name': 'Status Test Product', 'price': 10.0, 'quantity': 1}}
        add_order("status@example.com", "Address", cart)
        orders = get_orders()
        if orders:
            order_id = orders[-1]['id']
            update_order_status(order_id, "Shipped")
            order, _ = get_order_details(order_id)
            assert order['status'] == "Shipped"

    def test_delete_order(self):
        """Test deleting an order."""
        # Create a product first
        from models import create_product
        product_id = create_product("Delete Test Product", 10.0)
        cart = {str(product_id): {'id': product_id, 'name': 'Delete Test Product', 'price': 10.0, 'quantity': 1}}
        add_order("delete@example.com", "Address", cart)
        orders_before = get_orders()
        if orders_before:
            order_id = orders_before[-1]['id']
            delete_order(order_id)
            orders_after = get_orders()
            assert len(orders_after) < len(orders_before)


class TestPromoCodeFunctions:
    """Unit tests for promo code functions."""

    def test_create_promo_code_success(self):
        """Test successful promo code creation."""
        success = create_promo_code("TESTCODE_UNIQUE", 10.0)
        assert success

    def test_create_promo_code_duplicate(self):
        """Test creating duplicate promo code fails."""
        create_promo_code("DUPLICATE_UNIQUE", 15.0)
        success = create_promo_code("DUPLICATE_UNIQUE", 20.0)
        assert not success

    def test_get_promo_code_active(self):
        """Test getting active promo code."""
        create_promo_code("ACTIVE_UNIQUE", 25.0)
        promo = get_promo_code("ACTIVE_UNIQUE")
        assert promo is not None
        assert promo['discount_percent'] == 25.0

    def test_get_promo_code_inactive(self):
        """Test getting inactive promo code returns None."""
        create_promo_code("INACTIVE_UNIQUE", 30.0)
        # Get the actual ID of the created code
        codes = get_all_promo_codes()
        code_id = None
        for code in codes:
            if code['code'] == 'INACTIVE_UNIQUE':
                code_id = code['id']
                break
        assert code_id is not None
        update_promo_code_status(code_id, False)
        promo = get_promo_code("INACTIVE_UNIQUE")
        assert promo is None

    def test_get_promo_code_nonexistent(self):
        """Test getting nonexistent promo code."""
        promo = get_promo_code("NONEXISTENT_UNIQUE")
        assert promo is None

    def test_apply_promo_discount(self):
        """Test applying promo discount."""
        create_promo_code("DISCOUNT10_UNIQUE", 10.0)
        total = 100.0
        discounted_total, discount_amount, error = apply_promo_discount(total, "DISCOUNT10_UNIQUE")
        assert error is None
        assert discounted_total == 90.0
        assert discount_amount == 10.0

    def test_apply_promo_discount_invalid_code(self):
        """Test applying invalid promo code."""
        total = 100.0
        discounted_total, discount_amount, error = apply_promo_discount(total, "INVALID_UNIQUE")
        assert error == "Недійсний промокод"
        assert discounted_total == total
        assert discount_amount == 0

    def test_update_promo_code_status(self):
        """Test updating promo code status."""
        create_promo_code("STATUS_UNIQUE", 5.0)
        # Get the ID of the created code
        codes = get_all_promo_codes()
        code_id = None
        for code in codes:
            if code['code'] == 'STATUS_UNIQUE':
                code_id = code['id']
                break
        assert code_id is not None

        success = update_promo_code_status(code_id, False)
        assert success
        promo = get_promo_code("STATUS_UNIQUE")
        assert promo is None  # Should be inactive

    def test_delete_promo_code(self):
        """Test deleting promo code."""
        create_promo_code("DELETE_UNIQUE", 12.0)
        codes_before = get_all_promo_codes()
        # Get the ID
        code_id = None
        for code in codes_before:
            if code['code'] == 'DELETE_UNIQUE':
                code_id = code['id']
                break
        assert code_id is not None

        success = delete_promo_code(code_id)
        assert success
        codes_after = get_all_promo_codes()
        assert len(codes_after) < len(codes_before)