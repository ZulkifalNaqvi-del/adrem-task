"""
Pytest Configuration File
Contains fixtures and hooks for test execution
"""
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from utils.logger import Logger
from utils.test_data_reader import TestDataReader
from utils.screenshot_handler import ScreenshotHandler

logger = Logger.get_logger(__name__)


def pytest_configure(config):
    """Pytest configuration hook"""
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("TEST EXECUTION STARTED")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


def pytest_unconfigure(config):
    """Pytest cleanup hook"""
    logger.info("=" * 80)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)


@pytest.fixture(scope="session")
def test_data():
    """
    Fixture to provide test data
    Scope: session (loaded once per test session)
    """
    logger.info("Loading test data")
    data_reader = TestDataReader()
    return data_reader


@pytest.fixture(scope="session")
def base_url(test_data):
    """
    Fixture to provide base URL
    Scope: session
    """
    url = test_data.get_test_config()['base_url']
    logger.info(f"Base URL: {url}")
    return url


@pytest.fixture(scope="function")
def driver(request, test_data):
    """
    Fixture to provide WebDriver instance
    Scope: function (new driver for each test)
    
    Implements Fail Fast principle with proper setup and teardown
    """
    config = test_data.get_test_config()
    
    logger.info("Initializing WebDriver")
    
    # Chrome Options
    chrome_options = Options()
    
    if config.get('headless', False):
        chrome_options.add_argument('--headless')
        logger.info("Running in headless mode")
    
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize WebDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(config.get('implicit_wait', 10))
        driver.maximize_window()
        
        logger.info("WebDriver initialized successfully")
        
        # Navigate to base URL
        base_url = config['base_url']
        driver.get(base_url)
        logger.info(f"Navigated to: {base_url}")
        
        # Provide driver to test
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise
    
    finally:
        # Teardown - Close browser
        logger.info("Closing WebDriver")
        if driver:
            driver.quit()
            logger.info("WebDriver closed successfully")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    """
    Fixture to capture screenshot on test failure
    Implements Fail Fast principle with detailed failure reporting
    """
    yield
    
    # Check if test failed
    if request.node.rep_call.failed:
        test_name = request.node.name
        logger.error(f"Test FAILED: {test_name}")
        
        # Capture screenshot
        try:
            screenshot_handler = ScreenshotHandler(driver)
            screenshot_path = screenshot_handler.capture_failure_screenshot(test_name)
            logger.info(f"Failure screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to make test result available to fixtures
    Used for screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def logged_in_driver(driver, test_data):
    """
    Fixture to provide driver with user already logged in
    Useful for tests that require authentication
    Creates a new user account first, then logs in
    """
    from pages.login_page import LoginPage
    from pages.registration_page import RegistrationPage
    
    logger.info("Setting up logged in driver - registering new user first")
    
    credentials = test_data.get_user_credentials()
    registration_page = RegistrationPage(driver)
    
    # Register the user first
    registration_page.navigate_to_registration_page()
    reg_success = registration_page.register_new_user(
        first_name=credentials['first_name'],
        last_name=credentials['last_name'],
        email=credentials['email'],
        password=credentials['password'],
        gender='male'
    )
    
    if not reg_success:
        logger.error("Registration failed in fixture")
        raise Exception("Failed to register user in fixture")
    
    logger.info(f"User registered successfully in fixture: {credentials['email']}")
    
    # User should already be logged in after registration
    # But let's verify
    login_page = LoginPage(driver)
    if not login_page.is_logged_in():
        # If not logged in, perform login
        logger.info("User not logged in after registration, logging in now")
        success = login_page.login(
            credentials['email'],
            credentials['password']
        )
        
        if not success:
            logger.error("Login failed in fixture")
            raise Exception("Failed to login in fixture")
    
    logger.info("User logged in successfully in fixture")
    yield driver


@pytest.fixture(scope="function")
def cart_with_items(logged_in_driver, test_data):
    """
    Fixture to provide driver with items already in cart
    Useful for checkout tests
    """
    from pages.home_page import HomePage
    from pages.product_page import ProductPage
    
    logger.info("Setting up cart with items")
    
    home_page = HomePage(logged_in_driver)
    product_page = ProductPage(logged_in_driver)
    
    # Search and add products
    products = test_data.get_products_to_search()
    added_count = 0
    
    for product in products[:2]:  # Add first 2 products
        try:
            home_page.search_product(product)
            
            if product_page.get_search_results_count() > 0:
                product_page.add_to_cart_from_listing(0)
                added_count += 1
                logger.info(f"Added product to cart: {product}")
                
                # Return to home
                home_page.click_logo()
        except Exception as e:
            logger.warning(f"Failed to add product {product}: {e}")
    
    logger.info(f"Cart setup complete with {added_count} items")
    yield logged_in_driver


# Markers for test organization
def pytest_collection_modifyitems(items):
    """Modify test items to add markers based on test names"""
    for item in items:
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)
        if "cart" in item.nodeid.lower():
            item.add_marker(pytest.mark.cart)
        if "checkout" in item.nodeid.lower():
            item.add_marker(pytest.mark.checkout)

