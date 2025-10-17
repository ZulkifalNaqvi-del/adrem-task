"""
Registration Page Object Model
Handles user registration functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class RegistrationPage(BasePage):
    """Page Object for Registration Page - Single Responsibility Principle"""
    
    # Locators
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    GENDER_MALE = (By.ID, "gender-male")
    GENDER_FEMALE = (By.ID, "gender-female")
    FIRST_NAME = (By.ID, "FirstName")
    LAST_NAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    CONFIRM_PASSWORD = (By.ID, "ConfirmPassword")
    REGISTER_BUTTON = (By.ID, "register-button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".result")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, ".button-1.register-continue-button")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".field-validation-error")
    
    def __init__(self, driver):
        """Initialize RegistrationPage"""
        super().__init__(driver)
        logger.info("RegistrationPage initialized")
    
    def navigate_to_registration_page(self) -> None:
        """Navigate to registration page from homepage"""
        try:
            logger.info("Navigating to registration page")
            self.click(self.REGISTER_LINK)
            logger.info("Successfully navigated to registration page")
        except Exception as e:
            logger.error(f"Failed to navigate to registration page: {e}")
            self.capture_screenshot("navigation_to_register_failed")
            raise
    
    def select_gender(self, gender: str = "male") -> None:
        """
        Select gender radio button
        
        Args:
            gender: "male" or "female" (default: "male")
        """
        try:
            if gender.lower() == "male":
                self.click(self.GENDER_MALE)
                logger.info("Selected gender: Male")
            else:
                self.click(self.GENDER_FEMALE)
                logger.info("Selected gender: Female")
        except Exception as e:
            logger.error(f"Failed to select gender: {e}")
            raise
    
    def fill_registration_form(self, first_name: str, last_name: str, 
                               email: str, password: str, gender: str = "male") -> None:
        """
        Fill complete registration form
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            password: User's password
            gender: User's gender (default: "male")
        """
        try:
            logger.info(f"Filling registration form for user: {email}")
            
            # Select gender
            self.select_gender(gender)
            
            # Fill personal information
            self.send_keys(self.FIRST_NAME, first_name)
            logger.debug(f"Entered first name: {first_name}")
            
            self.send_keys(self.LAST_NAME, last_name)
            logger.debug(f"Entered last name: {last_name}")
            
            self.send_keys(self.EMAIL, email)
            logger.debug(f"Entered email: {email}")
            
            # Fill password fields
            self.send_keys(self.PASSWORD, password)
            logger.debug("Entered password")
            
            self.send_keys(self.CONFIRM_PASSWORD, password)
            logger.debug("Entered confirm password")
            
            logger.info("Registration form filled successfully")
            
        except Exception as e:
            logger.error(f"Failed to fill registration form: {e}")
            self.capture_screenshot("registration_form_fill_failed")
            raise
    
    def click_register_button(self) -> None:
        """Click the Register button to submit form"""
        try:
            logger.info("Clicking Register button")
            self.click(self.REGISTER_BUTTON)
            logger.info("Register button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Register button: {e}")
            self.capture_screenshot("register_button_click_failed")
            raise
    
    def get_success_message(self) -> str:
        """
        Get registration success message
        
        Returns:
            Success message text
        """
        try:
            message = self.get_text(self.SUCCESS_MESSAGE)
            logger.info(f"Registration success message: {message}")
            return message
        except Exception as e:
            logger.error(f"Failed to get success message: {e}")
            self.capture_screenshot("success_message_not_found")
            raise
    
    def is_registration_successful(self) -> bool:
        """
        Check if registration was successful
        
        Returns:
            True if success message is visible, False otherwise
        """
        try:
            return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=10)
        except Exception as e:
            logger.error(f"Error checking registration success: {e}")
            return False
    
    def click_continue_button(self) -> None:
        """Click Continue button after successful registration"""
        try:
            logger.info("Clicking Continue button")
            self.click(self.CONTINUE_BUTTON)
            logger.info("Continue button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Continue button: {e}")
            raise
    
    def get_validation_errors(self) -> list:
        """
        Get all validation error messages
        
        Returns:
            List of validation error messages
        """
        try:
            error_elements = self.find_elements(self.VALIDATION_ERROR)
            errors = [elem.text for elem in error_elements if elem.text]
            if errors:
                logger.warning(f"Validation errors found: {errors}")
            return errors
        except Exception as e:
            logger.error(f"Failed to get validation errors: {e}")
            return []
    
    def register_new_user(self, first_name: str, last_name: str, 
                         email: str, password: str, gender: str = "male") -> bool:
        """
        Complete user registration flow
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            password: User's password
            gender: User's gender (default: "male")
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            logger.info(f"Starting registration process for: {email}")
            
            self.navigate_to_registration_page()
            self.fill_registration_form(first_name, last_name, email, password, gender)
            self.click_register_button()
            
            # Wait for result
            if self.is_registration_successful():
                success_msg = self.get_success_message()
                self.capture_screenshot("registration_successful")
                logger.info(f"User registered successfully: {email}")
                return True
            else:
                errors = self.get_validation_errors()
                self.capture_screenshot("registration_failed")
                logger.error(f"Registration failed. Errors: {errors}")
                return False
                
        except Exception as e:
            logger.error(f"Registration process failed: {e}")
            self.capture_screenshot("registration_exception")
            raise

