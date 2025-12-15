# ParaBank Test Automation Framework

A comprehensive test automation framework for testing the ParaBank banking application using Python, Playwright, and pytest. This framework includes both UI and API testing capabilities with detailed reporting and CI/CD integration.

## Quick Start

### Prerequisites

- **Python 3.14+**
- **Node.js 20+** (for Playwright browsers)
- **Git**

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd demo-banking-website
   ```

2. **Install Poetry** (Python dependency manager)

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install all dependencies**

   ```bash
   poetry install
   ```

4. **Install Playwright browsers** (Required for UI tests)

   ```bash
   poetry run playwright install --with-deps chromium
   # Optional: Install all browsers
   poetry run playwright install --with-deps
   ```

5. **Configure test credentials**
   ```bash
   cp .env.example .env
   # Edit .env with your ParaBank test credentials:
   # USERNAME_1="your_test_username"
   # PASSWORD_1="your_test_password"
   # USER_FULLNAME_1="First Last"
   ```

## Running Tests

### Combined Test Execution

```bash
# Run ALL tests (UI + API)
poetry run pytest

# Run tests in parallel (faster execution)
poetry run pytest -n auto

# Run with maximum verbosity
poetry run pytest -v -s
```

### UI Tests (Browser Automation)

```bash
# Run all UI tests
poetry run pytest tests/UI/

# Run specific UI test files
poetry run pytest tests/UI/test_success_login.py
poetry run pytest tests/UI/test_transfer_funds.py
poetry run pytest tests/UI/test_view_account_details.py
poetry run pytest tests/UI/test_failed_login.py

# Run with specific browsers
poetry run pytest tests/UI/ --browser=chromium
poetry run pytest tests/UI/ --browser=firefox
poetry run pytest tests/UI/ --browser=webkit

# Debug mode (see browser actions)
poetry run pytest tests/UI/ --headed

# Run with slower execution for debugging
poetry run pytest tests/UI/ --headed --slowmo=1000
```

### API Tests (Backend Testing)

```bash
# Run all API tests
poetry run pytest tests/API/

# Run specific API test files
poetry run pytest tests/API/test_create_new_account.py
poetry run pytest tests/API/test_get_account_details.py
poetry run pytest tests/API/test_get_accounts_for_customer.py
poetry run pytest tests/API/test_create_account_with_invalid_from_account.py

# Run with verbose output
poetry run pytest tests/API/ -v

# Run with detailed output including print statements
poetry run pytest tests/API/ -s -v
```

## Allure Reporting Commands

### Generate Allure Reports

```bash
# Run tests and generate Allure data
poetry run pytest --alluredir=reports/allure

# Serve interactive Allure report (opens browser automatically)
allure serve reports/allure

# Generate static Allure report
allure generate reports/allure --output reports/allure-report --clean

# Open existing Allure report
allure open reports/allure-report
```

### Advanced Allure Usage

```bash
# Run specific tests with Allure
poetry run pytest tests/UI/test_success_login.py --alluredir=reports/allure
poetry run pytest tests/API/ --alluredir=reports/allure

# Combine with HTML reports
poetry run pytest --alluredir=reports/allure --html=reports/html/report.html --self-contained-html

# Run with custom Allure categories
poetry run pytest --alluredir=reports/allure --allure-categories=allure-categories.json
```

### Allure Features Available

- **Interactive dashboards** with test trends and statistics
- **Step-by-step execution** details with screenshots
- **API request/response** details and timing
- **Test history** and failure trends
- **Screenshots and traces** for failed tests
- **Test categorization** and filtering

## CI/CD Pipeline

### How the Pipeline Works

The GitHub Actions workflow ([`.github/workflows/test-automation.yml`](.github/workflows/test-automation.yml)) provides fully automated testing:

#### **Pipeline Triggers**

```yaml
on:
  push:
    branches: [main, develop] # Runs on every push to main/develop
  pull_request:
    types: [opened, synchronize, reopened] # Runs on every PR
```

#### **Pipeline Steps Overview**

1. **Environment Setup** (Automated)

   - ✅ Checkout code from repository
   - ✅ Install Python 3.14 and Node.js 20
   - ✅ Install Poetry dependency manager
   - ✅ Cache dependencies for faster builds

2. **Dependency Installation** (Automated)

   ```bash
   poetry install                                    # Install Python dependencies
   poetry run playwright install --with-deps chromium  # Install browser
   ```

3. **Test Execution** (Automated)

   ```bash
   poetry run pytest tests/ \
     --browser=chromium \
     --alluredir=reports/allure \
     --html=reports/html/report.html \
     --self-contained-html
   ```

4. **Report Generation** (Automated)

   - 📊 Allure interactive reports
   - 📄 HTML self-contained reports
   - 📸 Screenshots for failed tests
   - 🔍 Browser traces for debugging

5. **Artifact Storage** (30-day retention)
   - 💾 Test reports uploaded to GitHub
   - 🌐 Reports published to GitHub Pages
   - 📁 Available at: `https://<username>.github.io/<repo>/reports/<build-number>`

#### **Pipeline Environment Variables**

The pipeline uses encrypted secrets for test credentials:

```yaml
env:
  USERNAME_1: ${{ secrets.USERNAME_1 }} # Test user credentials
  PASSWORD_1: ${{ secrets.PASSWORD_1 }}
  USER_FULLNAME_1: ${{ secrets.USER_FULLNAME_1 }}
```

#### **Deployment to GitHub Pages**

Reports are automatically deployed and accessible via:

- **Latest Report**: `https://<username>.github.io/<repo>/reports/latest`
- **Specific Build**: `https://<username>.github.io/<repo>/reports/<build-number>`
- **Interactive Allure Dashboard** with full test history

## Project Structure

```
demo-banking-website/
├── .env                          # Environment variables
├── .env.example                  # Template for environment variables
├── conftest.py                   # Pytest configuration and fixtures
├── pyproject.toml                # Project dependencies and configuration
├── README.md                     # This file
├── .github/
│   └── workflows/
│       └── test-automation.yml   # CI/CD pipeline configuration
├── pages/                        # Page Object Models (UI)
│   ├── activity_page.py          # Account activity page
│   ├── base_page.py              # Base page class
│   ├── home_page.py              # Home page
│   ├── overview_page.py          # Account overview page
│   ├── transfer_page.py          # Fund transfer page
│   └── components/
│       └── customer_login.py     # Reusable login component
├── src/                          # Core framework components
│   ├── clients/
│   │   └── parabank_api_client.py    # API client wrapper
│   ├── enums/
│   │   └── account_types.py           # Account type definitions
│   ├── schemas/
│   │   └── parabank_schemas.py        # JSON validation schemas
│   ├── services/
│   │   └── response_validation_service.py  # API response validation
│   └── utils/
│       ├── currency_utils.py          # Currency formatting utilities
│       ├── encoding_utils.py          # Encoding utilities
│       └── schema_validator.py        # JSON schema validation
├── tests/
│   ├── API/                      # API test cases
│   │   ├── test_create_account_with_invalid_from_account.py
│   │   ├── test_create_new_account.py
│   │   ├── test_get_account_details.py
│   │   └── test_get_accounts_for_customer.py
│   └── UI/                       # UI test cases
│       ├── test_failed_login.py
│       ├── test_success_login.py
│       ├── test_transfer_funds.py
│       └── test_view_account_details.py
├── reports/                      # Test reports (auto-generated)
└── test-results/                 # Test artifacts (screenshots, traces)
```

## Features

### Framework Capabilities

- **Page Object Model (POM)**: Maintainable UI test structure
- **API Client Wrapper**: Simplified banking operations
- **Response Validation**: Automated JSON schema validation
- **Visual Testing**: Screenshots on test failures
- **Request Tracing**: Detailed network activity capture

### Reporting & Observability

- **Allure Reports**: Rich interactive test reports
- **HTML Reports**: Self-contained test reports
- **Screenshots**: Automatic capture on failures
- **Request Traces**: Detailed debugging information
- **CI/CD Integration**: Automated report publishing to GitHub Pages

## API Client Usage

The [`ParaBankAPIClient`](src/clients/parabank_api_client.py) provides a clean interface for banking operations:

```python
with ParaBankAPIClient(base_url=base_url, user_data=user_data) as api_client:
    # Get customer information
    customer_id = api_client.get_customer_id(username, password)

    # Account operations
    accounts = api_client.get_accounts_by_customer_id(customer_id)
    account_details = api_client.get_account_details(account_id)

    # Financial operations
    api_client.transfer_funds(from_account_id, to_account_id, amount)
    api_client.deposit_funds(account_id, amount)
    api_client.withdraw_funds(account_id, amount)

    # Account management
    new_account = api_client.create_account(customer_id, from_account_id, AccountType.SAVINGS)
```

## Page Objects

UI tests use the Page Object Model pattern for maintainability:

```python
from pages.home_page import HomePage
from pages.transfer_page import TransferPage

# Initialize page objects
home_page = HomePage(page, base_url)
transfer_page = TransferPage(page, base_url)

# Perform actions
home_page.login(username, password)
transfer_page.transfer_funds(amount=100, from_account_id=123, to_account_id=456)
```

## Schema Validation

API responses are automatically validated against JSON schemas:

```python
from src.services.response_validation_service import ResponseValidationService
from src.schemas.parabank_schemas import ParaBankSchemas

validator = ResponseValidationService()
validation_result = validator.validate_response(
    response_data,
    ParaBankSchemas.get_account_schema()
)

assert validation_result["valid"], f"Validation failed: {validation_result['errors']}"
```
