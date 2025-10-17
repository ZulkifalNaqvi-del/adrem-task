"""
Checkout Page Object Model
Handles checkout process including billing, shipping, payment, and confirmation
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger
import time

logger = Logger.get_logger(__name__)


class CheckoutPage(BasePage):
    """Page Object for Checkout Page - Single Responsibility Principle"""
    
    # Billing Address Locators
    BILLING_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#billing-buttons-container .button-1.new-address-next-step-button")
    BILLING_FIRST_NAME = (By.ID, "BillingNewAddress_FirstName")
    BILLING_LAST_NAME = (By.ID, "BillingNewAddress_LastName")
    BILLING_EMAIL = (By.ID, "BillingNewAddress_Email")
    BILLING_COMPANY = (By.ID, "BillingNewAddress_Company")
    BILLING_COUNTRY = (By.ID, "BillingNewAddress_CountryId")
    BILLING_CITY = (By.ID, "BillingNewAddress_City")
    BILLING_ADDRESS1 = (By.ID, "BillingNewAddress_Address1")
    BILLING_ADDRESS2 = (By.ID, "BillingNewAddress_Address2")
    BILLING_ZIP = (By.ID, "BillingNewAddress_ZipPostalCode")
    BILLING_PHONE = (By.ID, "BillingNewAddress_PhoneNumber")
    
    # Shipping Address Locators
    SHIPPING_CONTINUE_BUTTON = (By.CSS_SELECTOR, "#shipping-buttons-container .button-1.new-address-next-step-button")
    SHIP_TO_SAME_ADDRESS_CHECKBOX = (By.ID, "ShipToSameAddress")
    
    # Shipping Method Locators
    SHIPPING_METHOD_CONTINUE = (By.CSS_SELECTOR, "#shipping-method-buttons-container .button-1.shipping-method-next-step-button")
    GROUND_SHIPPING = (By.ID, "shippingoption_0")
    NEXT_DAY_AIR = (By.ID, "shippingoption_1")
    SECOND_DAY_AIR = (By.ID, "shippingoption_2")
    
    # Payment Method Locators
    PAYMENT_METHOD_CONTINUE = (By.CSS_SELECTOR, "#payment-method-buttons-container .button-1.payment-method-next-step-button")
    CASH_ON_DELIVERY = (By.ID, "paymentmethod_0")
    CHECK_MONEY_ORDER = (By.ID, "paymentmethod_1")
    CREDIT_CARD = (By.ID, "paymentmethod_2")
    PURCHASE_ORDER = (By.ID, "paymentmethod_3")
    
    # Payment Information Locators
    PAYMENT_INFO_CONTINUE = (By.CSS_SELECTOR, "#payment-info-buttons-container .button-1.payment-info-next-step-button")
    
    # Confirm Order Locators
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "#confirm-order-buttons-container .button-1.confirm-order-next-step-button")
    
    # Order Confirmation
    ORDER_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".section.order-completed .title strong")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-number")
    ORDER_DETAILS_LINK = (By.LINK_TEXT, "Click here for order details.")
    CONTINUE_BUTTON_FINAL = (By.CSS_SELECTOR, ".button-1.order-completed-continue-button")
    
    # Order Summary (visible throughout checkout)
    ORDER_SUMMARY_PRODUCTS = (By.CSS_SELECTOR, ".cart-item-row .product")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".cart-total-right .value-summary strong")
    
    def __init__(self, driver):
        """Initialize CheckoutPage"""
        super().__init__(driver)
        logger.info("CheckoutPage initialized")
    
    def fill_billing_address(self, address_data: dict) -> None:
        """
        Fill billing address form
        
        Args:
            address_data: Dictionary containing address information
        """
        try:
            logger.info("Filling billing address")
            
            self.send_keys(self.BILLING_FIRST_NAME, address_data.get('first_name', ''))
            self.send_keys(self.BILLING_LAST_NAME, address_data.get('last_name', ''))
            self.send_keys(self.BILLING_EMAIL, address_data.get('email', ''))
            
            if address_data.get('company'):
                self.send_keys(self.BILLING_COMPANY, address_data['company'])
            
            self.select_dropdown_by_text(self.BILLING_COUNTRY, address_data.get('country', 'United States'))
            
            self.send_keys(self.BILLING_CITY, address_data.get('city', ''))
            self.send_keys(self.BILLING_ADDRESS1, address_data.get('address1', ''))
            
            if address_data.get('address2'):
                self.send_keys(self.BILLING_ADDRESS2, address_data['address2'])
            
            self.send_keys(self.BILLING_ZIP, address_data.get('zip_code', ''))
            self.send_keys(self.BILLING_PHONE, address_data.get('phone', ''))
            
            logger.info("Billing address filled successfully")
            
        except Exception as e:
            logger.error(f"Failed to fill billing address: {e}")
            self.capture_screenshot("billing_address_failed")
            raise
    
    def click_billing_continue(self) -> None:
        """Click Continue button on billing address step"""
        try:
            logger.info("Clicking billing continue button")
            time.sleep(1)  # Small wait for form validation
            self.click(self.BILLING_CONTINUE_BUTTON)
            logger.info("Billing address submitted")
            time.sleep(2)  # Wait for next step to load
        except Exception as e:
            logger.error(f"Failed to click billing continue: {e}")
            self.capture_screenshot("billing_continue_failed")
            raise
    
    def click_shipping_continue(self) -> None:
        """Click Continue button on shipping address step"""
        try:
            logger.info("Clicking shipping continue button")
            time.sleep(1)
            self.click(self.SHIPPING_CONTINUE_BUTTON)
            logger.info("Shipping address submitted")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to click shipping continue: {e}")
            self.capture_screenshot("shipping_continue_failed")
            raise
    
    def select_shipping_method(self, method: str = "ground") -> None:
        """
        Select shipping method
        
        Args:
            method: Shipping method (ground, next_day, second_day)
        """
        try:
            logger.info(f"Selecting shipping method: {method}")
            
            method_lower = method.lower()
            if method_lower == "ground":
                self.click(self.GROUND_SHIPPING)
            elif method_lower == "next_day":
                self.click(self.NEXT_DAY_AIR)
            elif method_lower == "second_day":
                self.click(self.SECOND_DAY_AIR)
            else:
                logger.warning(f"Unknown shipping method: {method}, defaulting to ground")
                self.click(self.GROUND_SHIPPING)
            
            logger.info(f"Selected shipping method: {method}")
            
        except Exception as e:
            logger.error(f"Failed to select shipping method: {e}")
            raise
    
    def click_shipping_method_continue(self) -> None:
        """Click Continue button on shipping method step"""
        try:
            logger.info("Clicking shipping method continue button")
            time.sleep(1)
            self.click(self.SHIPPING_METHOD_CONTINUE)
            logger.info("Shipping method submitted")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to click shipping method continue: {e}")
            self.capture_screenshot("shipping_method_continue_failed")
            raise
    
    def select_payment_method(self, method: str = "cash") -> None:
        """
        Select payment method
        
        Args:
            method: Payment method (cash, check, credit_card, purchase_order)
        """
        try:
            logger.info(f"Selecting payment method: {method}")
            
            method_lower = method.lower()
            if method_lower == "cash":
                self.click(self.CASH_ON_DELIVERY)
            elif method_lower == "check":
                self.click(self.CHECK_MONEY_ORDER)
            elif method_lower == "credit_card":
                self.click(self.CREDIT_CARD)
            elif method_lower == "purchase_order":
                self.click(self.PURCHASE_ORDER)
            else:
                logger.warning(f"Unknown payment method: {method}, defaulting to cash")
                self.click(self.CASH_ON_DELIVERY)
            
            logger.info(f"Selected payment method: {method}")
            
        except Exception as e:
            logger.error(f"Failed to select payment method: {e}")
            raise
    
    def click_payment_method_continue(self) -> None:
        """Click Continue button on payment method step"""
        try:
            logger.info("Clicking payment method continue button")
            time.sleep(1)
            self.click(self.PAYMENT_METHOD_CONTINUE)
            logger.info("Payment method submitted")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to click payment method continue: {e}")
            self.capture_screenshot("payment_method_continue_failed")
            raise
    
    def click_payment_info_continue(self) -> None:
        """Click Continue button on payment information step"""
        try:
            logger.info("Clicking payment info continue button")
            time.sleep(1)
            self.click(self.PAYMENT_INFO_CONTINUE)
            logger.info("Payment info submitted")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to click payment info continue: {e}")
            self.capture_screenshot("payment_info_continue_failed")
            raise
    
    def click_confirm_order(self) -> None:
        """Click Confirm button to complete order"""
        try:
            logger.info("Clicking confirm order button")
            time.sleep(1)
            self.click(self.CONFIRM_BUTTON)
            logger.info("Order confirmed")
            time.sleep(3)  # Wait for order processing
        except Exception as e:
            logger.error(f"Failed to click confirm order: {e}")
            self.capture_screenshot("confirm_order_failed")
            raise
    
    def get_order_success_message(self) -> str:
        """
        Get order success message
        
        Returns:
            Order success message text
        """
        try:
            message = self.get_text(self.ORDER_SUCCESS_MESSAGE)
            logger.info(f"Order success message: {message}")
            return message
        except Exception as e:
            logger.error(f"Failed to get order success message: {e}")
            return ""
    
    def get_order_number(self) -> str:
        """
        Get order number from confirmation page
        
        Returns:
            Order number
        """
        try:
            order_text = self.get_text(self.ORDER_NUMBER)
            logger.info(f"Order number: {order_text}")
            return order_text
        except Exception as e:
            logger.error(f"Failed to get order number: {e}")
            return ""
    
    def is_order_completed(self) -> bool:
        """
        Check if order is completed successfully
        
        Returns:
            True if order success message is visible, False otherwise
        """
        try:
            is_completed = self.is_element_visible(self.ORDER_SUCCESS_MESSAGE, timeout=10)
            logger.info(f"Order completed status: {is_completed}")
            return is_completed
        except Exception as e:
            logger.error(f"Error checking order completion: {e}")
            return False
    
    def complete_checkout_flow(self, billing_address: dict, 
                               shipping_method: str = "ground",
                               payment_method: str = "cash") -> bool:
        """
        Complete entire checkout flow
        
        Args:
            billing_address: Dictionary with billing address data
            shipping_method: Shipping method to select
            payment_method: Payment method to select
            
        Returns:
            True if checkout completed successfully, False otherwise
        """
        try:
            logger.info("Starting complete checkout flow")
            
            # Step 1: Billing Address
            self.fill_billing_address(billing_address)
            self.click_billing_continue()
            
            # Step 2: Shipping Address (using same as billing)
            self.click_shipping_continue()
            
            # Step 3: Shipping Method
            self.select_shipping_method(shipping_method)
            self.click_shipping_method_continue()
            
            # Step 4: Payment Method
            self.select_payment_method(payment_method)
            self.click_payment_method_continue()
            
            # Step 5: Payment Information
            self.click_payment_info_continue()
            
            # Step 6: Confirm Order
            self.click_confirm_order()
            
            # Verify order completion
            if self.is_order_completed():
                order_msg = self.get_order_success_message()
                order_num = self.get_order_number()
                self.capture_screenshot("order_completed_successfully")
                logger.info(f"Checkout completed successfully. {order_num}")
                return True
            else:
                logger.error("Order completion verification failed")
                self.capture_screenshot("order_completion_failed")
                return False
                
        except Exception as e:
            logger.error(f"Checkout flow failed: {e}")
            self.capture_screenshot("checkout_flow_exception")
            raise
    
    def get_order_summary_products(self) -> list:
        """
        Get products from order summary
        
        Returns:
            List of product names
        """
        try:
            product_elements = self.find_elements(self.ORDER_SUMMARY_PRODUCTS)
            products = [elem.text for elem in product_elements if elem.text]
            logger.info(f"Order summary products: {products}")
            return products
        except Exception as e:
            logger.error(f"Failed to get order summary products: {e}")
            return []

