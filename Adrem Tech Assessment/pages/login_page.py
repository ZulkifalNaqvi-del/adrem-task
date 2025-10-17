"""
Login Page Object Model
Handles user authentication functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class LoginPage(BasePage):
    """Page Object for Login Page - Single Responsibility Principle"""
    
    # Locators
    LOGIN_LINK = (By.LINK_TEXT, "Log in")
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    REMEMBER_ME_CHECKBOX = (By.ID, "RememberMe")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".button-1.login-button")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    ACCOUNT_LINK = (By.LINK_TEXT, "My account")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".message-error")
    VALIDATION_SUMMARY = (By.CSS_SELECTOR, ".validation-summary-errors")
    
    def __init__(self, driver):
        """Initialize LoginPage"""
        super().__init__(driver)
        logger.info("LoginPage initialized")
    
    def navigate_to_login_page(self) -> None:
        """Navigate to login page from homepage"""
        try:
            logger.info("Navigating to login page")
            self.click(self.LOGIN_LINK)
            logger.info("Successfully navigated to login page")
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {e}")
            self.capture_screenshot("navigation_to_login_failed")
            raise
    
    def enter_email(self, email: str) -> None:
        """
        Enter email address
        
        Args:
            email: User's email address
        """
        try:
            self.send_keys(self.EMAIL_INPUT, email)
            logger.info(f"Entered email: {email}")
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")
            raise
    
    def enter_password(self, password: str) -> None:
        """
        Enter password
        
        Args:
            password: User's password
        """
        try:
            self.send_keys(self.PASSWORD_INPUT, password)
            logger.info("Entered password")
        except Exception as e:
            logger.error(f"Failed to enter password: {e}")
            raise
    
    def check_remember_me(self) -> None:
        """Check the Remember Me checkbox"""
        try:
            self.click(self.REMEMBER_ME_CHECKBOX)
            logger.info("Checked Remember Me checkbox")
        except Exception as e:
            logger.warning(f"Failed to check Remember Me: {e}")
    
    def click_login_button(self) -> None:
        """Click the Login button"""
        try:
            logger.info("Clicking Login button")
            self.click(self.LOGIN_BUTTON)
            logger.info("Login button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click Login button: {e}")
            self.capture_screenshot("login_button_click_failed")
            raise
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in
        
        Returns:
            True if logged in (Logout link visible), False otherwise
        """
        try:
            is_logged_in = self.is_element_visible(self.LOGOUT_LINK, timeout=5)
            logger.info(f"User logged in status: {is_logged_in}")
            return is_logged_in
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False
    
    def get_error_message(self) -> str:
        """
        Get login error message
        
        Returns:
            Error message text or empty string if no error
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
                message = self.get_text(self.ERROR_MESSAGE)
                logger.warning(f"Login error message: {message}")
                return message
            return ""
        except Exception as e:
            logger.error(f"Failed to get error message: {e}")
            return ""
    
    def get_validation_errors(self) -> str:
        """
        Get validation error summary
        
        Returns:
            Validation error text or empty string if no errors
        """
        try:
            if self.is_element_visible(self.VALIDATION_SUMMARY, timeout=5):
                message = self.get_text(self.VALIDATION_SUMMARY)
                logger.warning(f"Validation errors: {message}")
                return message
            return ""
        except Exception as e:
            logger.error(f"Failed to get validation errors: {e}")
            return ""
    
    def login(self, email: str, password: str, remember_me: bool = False) -> bool:
        """
        Perform complete login operation
        
        Args:
            email: User's email address
            password: User's password
            remember_me: Whether to check Remember Me checkbox (default: False)
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info(f"Starting login process for user: {email}")
            
            self.navigate_to_login_page()
            self.enter_email(email)
            self.enter_password(password)
            
            if remember_me:
                self.check_remember_me()
            
            self.click_login_button()
            
            # Check if login was successful
            if self.is_logged_in():
                self.capture_screenshot("login_successful")
                logger.info(f"User logged in successfully: {email}")
                return True
            else:
                error_msg = self.get_error_message()
                validation_errors = self.get_validation_errors()
                self.capture_screenshot("login_failed")
                logger.error(f"Login failed. Error: {error_msg} {validation_errors}")
                return False
                
        except Exception as e:
            logger.error(f"Login process failed: {e}")
            self.capture_screenshot("login_exception")
            raise
    
    def logout(self) -> bool:
        """
        Perform logout operation
        
        Returns:
            True if logout successful, False otherwise
        """
        try:
            if self.is_logged_in():
                logger.info("Logging out user")
                self.click(self.LOGOUT_LINK)
                
                # Check if logout was successful (Login link should be visible)
                if self.is_element_visible(self.LOGIN_LINK, timeout=5):
                    logger.info("User logged out successfully")
                    return True
                else:
                    logger.error("Logout may have failed")
                    return False
            else:
                logger.warning("User is not logged in, cannot logout")
                return False
                
        except Exception as e:
            logger.error(f"Logout process failed: {e}")
            self.capture_screenshot("logout_exception")
            raise
    
    def navigate_to_my_account(self) -> None:
        """Navigate to My Account page"""
        try:
            if self.is_logged_in():
                logger.info("Navigating to My Account page")
                self.click(self.ACCOUNT_LINK)
                logger.info("Successfully navigated to My Account page")
            else:
                logger.error("Cannot navigate to My Account - user not logged in")
                raise Exception("User not logged in")
        except Exception as e:
            logger.error(f"Failed to navigate to My Account: {e}")
            raise

