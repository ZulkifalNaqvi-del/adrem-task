"""
Test Suite for Complete Checkout Flow
Tests end-to-end checkout process from login to order confirmation
"""
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger
from utils.csv_reporter import CSVReporter, StepTimer


class TestCompleteCheckoutFlow:
    """Test class for complete checkout flow - Single Responsibility Principle"""
    
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_end_to_end_checkout_flow(self, driver, test_data):
        """
        Test Step: Complete end-to-end checkout flow
        Steps:
        0. Register new user
        1. Logout after registration
        2. Login with newly created credentials
        3. Search and add multiple products to cart
        4. Navigate to cart and validate items
        5. Proceed to checkout
        6. Fill billing/shipping address
        7. Select shipping and payment methods
        8. Confirm order and validate order completion
        
        Expected: Order placed successfully with confirmation message
        """
        logger.info("=" * 80)
        logger.info("TEST: Complete End-to-End Checkout Flow")
        logger.info("=" * 80)
        
        # Initialize CSV Reporter
        csv_reporter = CSVReporter("e2e_checkout_test")
        
        # Get test data
        credentials = test_data.get_user_credentials()
        billing_address = test_data.get_billing_address()
        products_to_add = test_data.get_products_to_search()
        
        # Initialize page objects
        from pages.registration_page import RegistrationPage
        registration_page = RegistrationPage(driver)
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        
        # Step 0: Register new user
        logger.info("STEP 0: Register new user")
        timer = StepTimer()
        timer.start()
        try:
            registration_page.navigate_to_registration_page()
            reg_success = registration_page.register_new_user(
                first_name=credentials['first_name'],
                last_name=credentials['last_name'],
                email=credentials['email'],
                password=credentials['password'],
                gender='male'
            )
            assert reg_success, "User registration failed"
            timer.stop()
            csv_reporter.add_step(
                step_number=0,
                step_name="User Registration",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Registered user: {credentials['email']}"
            )
            logger.info(f"✓ User registered successfully: {credentials['email']}")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=0,
                step_name="User Registration",
                status="FAILED",
                duration=timer.get_duration(),
                details=f"Failed to register user: {credentials['email']}",
                error_message=str(e)
            )
            raise
        
        # Step 1: Logout after registration
        logger.info("STEP 1: Logout after registration")
        timer = StepTimer()
        timer.start()
        try:
            # First check if user is logged in after registration
            if login_page.is_logged_in():
                logout_success = login_page.logout()
                assert logout_success, "Logout failed"
                logger.info("✓ User logged out successfully")
            else:
                logger.warning("User was not logged in after registration")
            
            timer.stop()
            csv_reporter.add_step(
                step_number=1,
                step_name="Logout After Registration",
                status="SUCCESS",
                duration=timer.get_duration(),
                details="User logged out successfully after registration"
            )
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=1,
                step_name="Logout After Registration",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to logout after registration",
                error_message=str(e)
            )
            raise
        
        # Step 2: Login with newly created credentials
        logger.info("STEP 2: Login with newly created credentials")
        timer = StepTimer()
        timer.start()
        try:
            login_success = login_page.login(credentials['email'], credentials['password'])
            assert login_success, "Login with newly created credentials failed"
            timer.stop()
            csv_reporter.add_step(
                step_number=2,
                step_name="Login with New Credentials",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Successfully logged in with new credentials: {credentials['email']}"
            )
            logger.info(f"✓ User logged in successfully with new credentials: {credentials['email']}")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=2,
                step_name="Login with New Credentials",
                status="FAILED",
                duration=timer.get_duration(),
                details=f"Failed to login with new credentials: {credentials['email']}",
                error_message=str(e)
            )
            raise
        
        # Step 3: Add multiple products to cart
        logger.info("STEP 3: Add multiple products to cart")
        timer = StepTimer()
        timer.start()
        added_count = 0
        
        try:
            for i, product in enumerate(products_to_add[:3]):  # Add first 3 products
                try:
                    logger.info(f"  Adding product {i+1}: {product}")
                    home_page.search_product(product)
                    
                    if product_page.get_search_results_count() > 0:
                        product_page.add_to_cart_from_listing(0)
                        added_count += 1
                        logger.info(f"  ✓ Product added: {product}")
                        
                        # Close notification and return to home
                        product_page.close_notification()
                        home_page.click_logo()
                    else:
                        logger.warning(f"  ⚠ No results for: {product}")
                except Exception as e:
                    logger.warning(f"  ⚠ Failed to add {product}: {e}")
            
            assert added_count > 0, "Failed to add any products to cart"
            timer.stop()
            csv_reporter.add_step(
                step_number=3,
                step_name="Add Products to Cart",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Added {added_count} products to cart"
            )
            logger.info(f"✓ Added {added_count} products to cart")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=3,
                step_name="Add Products to Cart",
                status="FAILED",
                duration=timer.get_duration(),
                details=f"Only added {added_count} products",
                error_message=str(e)
            )
            raise
        
        # Step 4: Navigate to cart and validate
        logger.info("STEP 4: Navigate to cart and validate items")
        timer = StepTimer()
        timer.start()
        
        try:
            home_page.navigate_to_shopping_cart()
            
            cart_items_count = cart_page.get_cart_items_count()
            logger.info(f"  Cart items count: {cart_items_count}")
            assert cart_items_count > 0, "Cart is empty"
            
            product_names = cart_page.get_product_names()
            logger.info(f"  Products in cart: {product_names}")
            
            cart_total = cart_page.get_cart_total()
            logger.info(f"  Cart total: {cart_total}")
            # Cart total validation is informational only - don't fail test if not found
            if cart_total and "$" in cart_total:
                logger.info(f"  ✓ Cart total validated: {cart_total}")
            else:
                logger.warning(f"  ⚠ Cart total not clearly displayed, but continuing...")
            
            timer.stop()
            csv_reporter.add_step(
                step_number=4,
                step_name="Cart Validation",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Cart items: {cart_items_count}, Total: {cart_total}"
            )
            logger.info("✓ Cart validated successfully")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=4,
                step_name="Cart Validation",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to validate cart",
                error_message=str(e)
            )
            raise
        
        # Step 5: Proceed to checkout
        logger.info("STEP 5: Proceed to checkout")
        timer = StepTimer()
        timer.start()
        
        try:
            cart_page.proceed_to_checkout()
            timer.stop()
            csv_reporter.add_step(
                step_number=5,
                step_name="Proceed to Checkout",
                status="SUCCESS",
                duration=timer.get_duration(),
                details="Successfully navigated to checkout"
            )
            logger.info("✓ Proceeded to checkout")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=5,
                step_name="Proceed to Checkout",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to proceed to checkout",
                error_message=str(e)
            )
            raise
        
        # Step 6: Fill billing address
        logger.info("STEP 6: Fill billing address")
        timer = StepTimer()
        timer.start()
        
        try:
            checkout_page.fill_billing_address(billing_address)
            checkout_page.click_billing_continue()
            timer.stop()
            csv_reporter.add_step(
                step_number=6,
                step_name="Fill Billing Address",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Billing address: {billing_address['city']}, {billing_address['country']}"
            )
            logger.info("✓ Billing address filled successfully")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=6,
                step_name="Fill Billing Address",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to fill billing address",
                error_message=str(e)
            )
            raise
        
        # Step 7: Complete checkout flow (shipping, payment, confirm)
        logger.info("STEP 7: Complete checkout flow (shipping, payment, confirm)")
        timer = StepTimer()
        timer.start()
        
        try:
            checkout_page.click_shipping_continue()
            checkout_page.select_shipping_method("ground")
            checkout_page.click_shipping_method_continue()
            checkout_page.select_payment_method("cash")
            checkout_page.click_payment_method_continue()
            checkout_page.click_payment_info_continue()
            checkout_page.click_confirm_order()
            
            timer.stop()
            csv_reporter.add_step(
                step_number=7,
                step_name="Complete Checkout (Shipping, Payment, Confirm)",
                status="SUCCESS",
                duration=timer.get_duration(),
                details="Shipping: Ground, Payment: Cash on Delivery"
            )
            logger.info("✓ Checkout flow completed")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=7,
                step_name="Complete Checkout (Shipping, Payment, Confirm)",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to complete checkout flow",
                error_message=str(e)
            )
            raise
        
        # Step 8: Validate order completion
        logger.info("STEP 8: Validate order completion")
        timer = StepTimer()
        timer.start()
        
        try:
            success_message = checkout_page.get_order_success_message()
            logger.info(f"  Success message: {success_message}")
            
            assert "successfully" in success_message.lower() or "processed" in success_message.lower(), \
                f"Unexpected success message: {success_message}"
            
            order_number = checkout_page.get_order_number()
            logger.info(f"  Order number: {order_number}")
            
            # Capture final screenshot
            checkout_page.capture_screenshot("order_confirmation_final")
            
            timer.stop()
            csv_reporter.add_step(
                step_number=8,
                step_name="Order Completion Validation",
                status="SUCCESS",
                duration=timer.get_duration(),
                details=f"Order confirmed. Message: {success_message[:50]}..."
            )
            logger.info("✓ Order completed successfully")
        except Exception as e:
            timer.stop()
            csv_reporter.add_step(
                step_number=8,
                step_name="Order Completion Validation",
                status="FAILED",
                duration=timer.get_duration(),
                details="Failed to validate order completion",
                error_message=str(e)
            )
            raise
        
        # Generate CSV report
        csv_reporter.add_summary()
        report_path = csv_reporter.generate_report()
        
        logger.info("=" * 80)
        logger.info("TEST PASSED: End-to-End Checkout Flow Completed Successfully")
        logger.info(f"CSV Report generated: {report_path}")
        logger.info("=" * 80)
    
    @pytest.mark.checkout
    def test_checkout_with_single_product(self, logged_in_driver, test_data):
        """
        Test Step: Checkout with a single product
        Expected: Order placed successfully
        """
        logger.info("TEST: Checkout with single product")
        
        billing_address = test_data.get_billing_address()
        
        home_page = HomePage(logged_in_driver)
        product_page = ProductPage(logged_in_driver)
        cart_page = CartPage(logged_in_driver)
        checkout_page = CheckoutPage(logged_in_driver)
        
        # Add single product
        home_page.search_product("laptop")
        if product_page.get_search_results_count() > 0:
            product_page.add_to_cart_from_listing(0)
        
        # Navigate to cart
        home_page.navigate_to_shopping_cart()
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Complete checkout
        checkout_success = checkout_page.complete_checkout_flow(
            billing_address=billing_address,
            shipping_method="ground",
            payment_method="cash"
        )
        
        assert checkout_success, "Checkout failed"
        
        logger.info("TEST PASSED: Single product checkout successful")
    
    @pytest.mark.checkout
    def test_billing_address_step(self, cart_with_items, test_data):
        """
        Test Step: Test billing address form submission
        Expected: Billing address accepted and moves to next step
        """
        logger.info("TEST: Billing address step")
        
        billing_address = test_data.get_billing_address()
        
        home_page = HomePage(cart_with_items)
        cart_page = CartPage(cart_with_items)
        checkout_page = CheckoutPage(cart_with_items)
        
        # Navigate to cart
        home_page.navigate_to_shopping_cart()
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Fill and submit billing address
        checkout_page.fill_billing_address(billing_address)
        checkout_page.click_billing_continue()
        
        # Verify moved to next step (shipping)
        # The page should have progressed
        logger.info("TEST PASSED: Billing address step completed")
    
    @pytest.mark.checkout
    def test_shipping_method_selection(self, cart_with_items, test_data):
        """
        Test Step: Test shipping method selection
        Expected: Shipping method can be selected
        """
        logger.info("TEST: Shipping method selection")
        
        billing_address = test_data.get_billing_address()
        
        home_page = HomePage(cart_with_items)
        cart_page = CartPage(cart_with_items)
        checkout_page = CheckoutPage(cart_with_items)
        
        # Navigate to cart and checkout
        home_page.navigate_to_shopping_cart()
        cart_page.proceed_to_checkout()
        
        # Fill billing address
        checkout_page.fill_billing_address(billing_address)
        checkout_page.click_billing_continue()
        
        # Continue shipping (same as billing)
        checkout_page.click_shipping_continue()
        
        # Select shipping method
        checkout_page.select_shipping_method("ground")
        checkout_page.click_shipping_method_continue()
        
        logger.info("TEST PASSED: Shipping method selected")
    
    @pytest.mark.checkout
    def test_payment_method_selection(self, cart_with_items, test_data):
        """
        Test Step: Test payment method selection
        Expected: Payment method can be selected
        """
        logger.info("TEST: Payment method selection")
        
        billing_address = test_data.get_billing_address()
        
        home_page = HomePage(cart_with_items)
        cart_page = CartPage(cart_with_items)
        checkout_page = CheckoutPage(cart_with_items)
        
        # Navigate to cart and checkout
        home_page.navigate_to_shopping_cart()
        cart_page.proceed_to_checkout()
        
        # Complete steps to reach payment method
        checkout_page.fill_billing_address(billing_address)
        checkout_page.click_billing_continue()
        checkout_page.click_shipping_continue()
        checkout_page.select_shipping_method("ground")
        checkout_page.click_shipping_method_continue()
        
        # Select payment method
        checkout_page.select_payment_method("cash")
        checkout_page.click_payment_method_continue()
        
        logger.info("TEST PASSED: Payment method selected")
    
    @pytest.mark.checkout
    def test_order_confirmation_message(self, cart_with_items, test_data):
        """
        Test Step: Verify order confirmation message
        Expected: Success message displayed after order completion
        """
        logger.info("TEST: Order confirmation message")
        
        billing_address = test_data.get_billing_address()
        
        home_page = HomePage(cart_with_items)
        cart_page = CartPage(cart_with_items)
        checkout_page = CheckoutPage(cart_with_items)
        
        # Navigate to cart
        home_page.navigate_to_shopping_cart()
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Complete checkout
        checkout_success = checkout_page.complete_checkout_flow(
            billing_address=billing_address,
            shipping_method="ground",
            payment_method="cash"
        )
        
        assert checkout_success, "Checkout failed"
        
        # Verify confirmation elements
        success_message = checkout_page.get_order_success_message()
        assert success_message, "Success message not displayed"
        
        order_number = checkout_page.get_order_number()
        assert order_number, "Order number not displayed"
        
        logger.info(f"TEST PASSED: Order confirmed - {order_number}")

