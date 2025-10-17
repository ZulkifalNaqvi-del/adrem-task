# E-Commerce Checkout Flow Automation

## 📋 Project Overview

This is a comprehensive test automation framework for the Demo Web Shop (https://demowebshop.tricentis.com/) e-commerce website. The framework implements end-to-end checkout flow automation using Selenium WebDriver, Python, and pytest.

## 🎯 Features

- **Page Object Model (POM)**: Clean, maintainable page object architecture
- **DRY Principle**: Reusable components and methods
- **Single Responsibility Principle**: Each class/method has a single, well-defined purpose
- **Fail Fast Principle**: Early detection of issues with explicit waits and assertions
- **Comprehensive Logging**: Detailed execution logs with color-coded console output
- **Screenshot Capture**: Automatic screenshots on failures and key steps
- **External Test Data**: JSON-based test data management with unique user generation
- **CSV Step Reports**: Detailed CSV reports for each test step with success/failure status
- **HTML Reports**: Beautiful test execution reports with pytest-html
- **Error Handling**: Try-catch blocks with detailed error logging

## 🏗️ Project Structure

```
Adrem Tech Assessment/
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py           # Base class with common methods (DRY)
│   ├── registration_page.py   # Registration page objects
│   ├── login_page.py          # Login page objects
│   ├── home_page.py           # Home page objects
│   ├── product_page.py        # Product search and detail page objects
│   ├── cart_page.py           # Shopping cart page objects
│   └── checkout_page.py       # Checkout flow page objects
│
├── tests/                      # Test cases
│   ├── __init__.py
│   └── test_05_complete_checkout_flow.py  # Complete E2E test with CSV reporting
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Centralized logging utility
│   ├── screenshot_handler.py  # Screenshot capture utility
│   ├── test_data_reader.py    # JSON test data reader
│   └── csv_reporter.py        # CSV test execution reporter
│
├── data/                       # Test data files
│   └── test_data.json         # User credentials, addresses, config
│
├── reports/                    # Test execution reports
│   ├── report.html            # HTML test report
│   ├── *.csv                  # CSV step-by-step execution reports
│   └── *.log                  # Execution logs
│
├── screenshots/                # Test screenshots
│   └── *.png                  # Captured screenshots
│
├── conftest.py                # Pytest fixtures and configuration
├── pytest.ini                 # Pytest settings
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Test Framework**: pytest 8.3.3
- **WebDriver**: Selenium 4.25.0
- **Browser**: Chrome (with WebDriver Manager)
- **Reporting**: pytest-html, Allure
- **Logging**: colorlog
- **Data Management**: JSON

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- pip (Python package manager)

### Setup Steps

1. **Clone or Extract the Project**
   ```bash
   cd "Adrem Tech Assessment"
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   pytest --version
   python -c "import selenium; print(selenium.__version__)"
   ```

## ⚙️ Configuration

### Test Data Configuration

Edit `data/test_data.json` to customize:

- **User Credentials**: Email, password, name
- **Billing/Shipping Address**: Complete address information
- **Test Configuration**: Browser settings, timeouts, URLs
- **Products to Search**: List of products for testing

**Note**: Each test run automatically generates unique user credentials using timestamp and random numbers, ensuring no conflicts between test runs.

### Browser Configuration

By default, tests run in Chrome with GUI. To run headless:

Edit `data/test_data.json`:
```json
"test_config": {
  "headless": true
}
```

## 🚀 Running Tests

### Quick Start (Easiest Method)
```bash
python run_tests.py
```

### Run All Tests
```bash
pytest
```

### Run the End-to-End Test (Recommended)
```bash
pytest tests/test_05_complete_checkout_flow.py -v -s
```

### Run Tests by Marker
```bash
# Run only smoke tests
pytest -m smoke

# Run only checkout tests
pytest -m checkout

# Run login tests
pytest -m login
```

### Run Specific Test
```bash
pytest tests/test_05_complete_checkout_flow.py::TestCompleteCheckoutFlow::test_end_to_end_checkout_flow
```

### Run with Verbose Output
```bash
pytest -v
```

### Run in Parallel (Faster Execution)
```bash
pytest -n 4  # Run with 4 workers
```

### Generate Allure Report
```bash
# Run tests with allure
pytest --alluredir=./allure-results

# Generate and open report
allure serve ./allure-results
```

## 📊 Test Reports

### CSV Step-by-Step Report (NEW!)

Each test run generates a detailed CSV report with step-by-step execution results:

**Location**: `reports/e2e_checkout_test_YYYYMMDD_HHMMSS.csv`

**CSV Report Includes**:
- **Step Number**: Sequential step number
- **Step Name**: Description of the test step
- **Status**: SUCCESS or FAILED
- **Duration**: Time taken in seconds
- **Details**: Additional information about the step
- **Error Message**: Detailed error message if step failed
- **Summary Row**: Total steps, passed, failed, and total duration

**Example CSV Output**:
```csv
Step Number,Step Name,Status,Duration (seconds),Details,Error Message
0,User Registration,SUCCESS,3.97,Registered user: testuser_1760709996_6041@example.com,
1,User Login Verification,SUCCESS,0.02,User logged in: testuser_1760709996_6041@example.com,
2,Add Products to Cart,SUCCESS,16.92,Added 3 products to cart,
3,Cart Validation,SUCCESS,13.51,"Cart items: 2, Total: 1600.00",
4,Proceed to Checkout,SUCCESS,1.6,Successfully navigated to checkout,
5,Fill Billing Address,SUCCESS,4.32,"Billing address: New York, United States",
6,"Complete Checkout (Shipping, Payment, Confirm)",SUCCESS,17.01,"Shipping: Ground, Payment: Cash on Delivery",
7,Order Completion Validation,SUCCESS,21.43,Order confirmed. Message: Your order has been successfully processed!...,
,SUMMARY,PASSED,78.78,"Total: 8, Passed: 8, Failed: 0",
```

**Test Steps Tracked**:
1. User Registration
2. User Login Verification  
3. Add Products to Cart
4. Cart Validation
5. Proceed to Checkout
6. Fill Billing Address
7. Complete Checkout (Shipping, Payment, Confirm)
8. Order Completion Validation

### HTML Report

After test execution, open `reports/report.html` in a browser to view:
- Test results summary
- Pass/fail status for each test
- Execution time
- Error messages and stack traces

### Log Files

Detailed logs are available in `reports/`:
- `automation_YYYYMMDD_HHMMSS.log` - Detailed execution log
- `test_execution.log` - Pytest execution log

### Screenshots

Screenshots are automatically captured:
- On test failures
- At key checkpoints (registration, login, cart, order confirmation)

Location: `screenshots/` directory

## 🧪 Test Scenarios Covered

### Complete End-to-End Checkout Flow (`test_05_complete_checkout_flow.py`)

The main test suite includes a comprehensive E2E test with CSV reporting:

✅ **Complete Checkout Flow with CSV Reporting**:
  1. **User Registration** - Register new user with unique credentials (timestamp-based)
  2. **Login Verification** - Verify user is logged in after registration
  3. **Add Products to Cart** - Search and add multiple products (laptop, book, smartphone)
  4. **Cart Validation** - Validate cart items count and total pricing
  5. **Proceed to Checkout** - Navigate to checkout page
  6. **Fill Billing Address** - Complete billing information form
  7. **Complete Checkout Steps** - Shipping address, shipping method, payment method
  8. **Order Confirmation** - Validate order success message and capture screenshot

**Key Features**:
- ✅ Each test step is tracked in CSV report with SUCCESS/FAILED status
- ✅ Detailed timing for each step (duration in seconds)
- ✅ Comprehensive error messages if any step fails
- ✅ Screenshots captured at critical points
- ✅ Summary row with total duration and pass/fail counts
- ✅ Unique user created for each test run (no conflicts)

## 🔧 Automation Principles Implemented

### DRY (Don't Repeat Yourself)
- **Base Page Class**: All common methods (click, send_keys, wait) in `base_page.py`
- **Reusable Utilities**: Logger, screenshot handler, data reader used across all tests
- **Fixtures**: Common setup/teardown in `conftest.py`

### SRP (Single Responsibility Principle)
- **Page Objects**: Each page class handles only its page's functionality
- **Test Classes**: Each test class focuses on specific feature area
- **Utility Classes**: Each utility has a single, well-defined purpose

### Fail Fast Principle
- **Explicit Waits**: Wait for elements before interaction
- **Assertions**: Validate at each step
- **Error Handling**: Try-catch blocks with detailed logging
- **Screenshots on Failure**: Immediate visual feedback

## 📝 Assumptions Made

1. **User Registration**: Each test run automatically creates a new user with unique credentials (timestamp + random number)
2. **Product Availability**: Tests assume products like "laptop", "book", "computer" exist on the site
3. **Browser**: Chrome browser is installed and accessible
4. **Internet Connection**: Stable connection to access the demo website
5. **Payment Methods**: Tests use "Cash on Delivery" as it doesn't require payment details
6. **Address**: Uses US addresses; country dropdown should have "United States" option

## 🐛 Troubleshooting

### Issue: WebDriver not found
**Solution**: 
```bash
pip install webdriver-manager --upgrade
```

### Issue: Tests timing out
**Solution**: Increase timeout in `data/test_data.json`:
```json
"test_config": {
  "implicit_wait": 15,
  "explicit_wait": 30
}
```

### Issue: Element not clickable
**Solution**: Tests already implement scrolling and explicit waits. Check if website structure changed.

### Issue: Test data user already exists
**Solution**: This issue is automatically handled - each test run generates unique credentials using timestamps and random numbers

## 📸 Screenshots

Key screenshots are captured at:
- User registration success
- Login success
- Product added to cart
- Order confirmation page (final confirmation screenshot)

## 🎓 Best Practices Followed

1. **Modular Design**: Page objects separated by responsibility
2. **Explicit Waits**: No hardcoded sleep() statements
3. **Logging**: Comprehensive logging at INFO, DEBUG, and ERROR levels
4. **Data-Driven**: Test data externalized in JSON
5. **Error Handling**: Graceful failure handling with screenshots
6. **Clean Code**: PEP 8 compliant Python code
7. **Git Ready**: Proper .gitignore for Python projects

## 📧 Contact & Support

For questions or issues with this automation framework, please refer to:
- Test execution logs in `reports/`
- Screenshots in `screenshots/`
- This README for setup instructions



---

**Note**: This framework demonstrates professional test automation practices suitable for enterprise-level test automation projects.

**Time Invested**: 2-3 days for complete framework development, including:
- Framework architecture design
- Page Object Model implementation
- Test case development
- Utilities and reporting setup
- Documentation

