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
   # Edit .env with your ParaBank test credentials and BASE_URL:
   # BASE_URL="base_url"
   # USERNAME_1="your_test_username"
   # PASSWORD_1="your_test_password"
   # USER_FULLNAME_1="First Last"
   ```

## Running Tests

### Combined Test Execution

```bash
# Run ALL tests (UI + API)
poetry run pytest

# Run with maximum verbosity
poetry run pytest -v -s
```

### UI Tests (Browser Automation)

```bash
# Run all UI tests
poetry run pytest tests/UI/

# Run specific UI test files
poetry run pytest tests/UI/test_success_login.py
...

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
...

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

#### **Database Initialization**

- A dedicated `initialize-database` job runs first to reset ParaBank test data via the public initialize endpoint.
- Uses `BASE_URL` from repository secrets, defaulting to `https://parabank.parasoft.com` if not set.
- Performs a POST to `/parabank/services/bank/initializeDB` with retries and fails the pipeline if HTTP status is not 200 or 204.

```yaml
initialize-database:
   runs-on: ubuntu-latest
   env:
      BASE_URL: ${{ secrets.BASE_URL || 'https://parabank.parasoft.com' }}
   steps:
      - name: Initialize ParaBank Database
         id: init-db
         run: |
            echo "Initializing ParaBank database..."

            response=$(curl -X POST "${{ env.BASE_URL }}/parabank/services/bank/initializeDB" \
               --silent \
               --write-out "HTTPSTATUS:%{http_code}" \
               --fail-with-body \
               --retry 3 \
               --retry-delay 5 \
               --max-time 60)

            http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

            if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 204 ]; then
               echo "✅ Database initialized successfully (HTTP: $http_code)"
            else
               echo "❌ Database initialization failed (HTTP: $http_code)"
               exit 1
            fi
```

#### **Pipeline Triggers**

```yaml
on:
  push:
    branches: [main, develop] # Runs on every push to main/develop
  pull_request:
    types: [opened, synchronize, reopened] # Runs on every PR
```

#### **Pipeline Environment Variables**

The pipeline uses encrypted secrets for test credentials:

```yaml
env:
  USERNAME_1: ${{ secrets.USERNAME_1 }} # Test user credentials
  PASSWORD_1: ${{ secrets.PASSWORD_1 }}
  USER_FULLNAME_1: ${{ secrets.USER_FULLNAME_1 }}
```

#### **Parallel Job Execution**

```yaml
jobs:
  api-tests:
    name: API Tests
    runs-on: ubuntu-latest
    ...

  ui-tests:
    name: UI Tests
    runs-on: ubuntu-latest
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

5. **Artifact Storage** (30-day retention)

   - 💾 Test reports uploaded to GitHub

6. **Deployment to GitHub Pages**
   - Reports are automatically deployed and accessible via:
     - **Latest Report**: `https://<username>.github.io/<repo>/reports/latest`
     - **Specific Build**: `https://<username>.github.io/<repo>/reports/<build-number>`

## Project Structure

```
demo-banking-website/
├── .env                              # Environment variables
├── .env.example                      # Template for environment variables
├── .github/
│   └── workflows/
│       └── test-automation.yml       # CI/CD pipeline configuration
├── conftest.py                       # Pytest configuration and fixtures
├── poetry.lock                       # Locked dependency versions
├── pyproject.toml                    # Project dependencies and configuration
├── README.md                         # This file
├── pages/                            # Page Object Models (UI)
│   ├── activity_page.py              # Account activity page
│   ├── base_page.py                  # Base page class and common helpers
│   ├── bill_payment_page.py          # Bill payment page
│   ├── find_transactions_page.py     # Find transactions page
│   ├── home_page.py                  # Home page
│   ├── open_account_page.py          # Open new account page
│   ├── overview_page.py              # Accounts overview page
│   ├── request_loan_page.py          # Request loan page
│   ├── transfer_page.py              # Transfer funds page
│   ├── update_profile_page.py        # Update contact/profile info page
│   └── components/                   # Reusable UI components
│       ├── customer_login.py         # Login form component
│       └── left_navigation_panel.py  # Left navigation menu
├── src/                              # Core framework utilities and services
│   ├── clients/
│   │   └── parabank_api_client.py    # API client wrapper
│   ├── enums/
│   │   ├── account_types.py          # Account type definitions
│   │   └── transaction_types.py      # Transaction type definitions
│   ├── schemas/
│   │   └── parabank_schemas.py       # JSON validation schemas
│   ├── services/
│   │   └── response_validation_service.py  # API response validation
│   └── utils/
│       ├── currency_utils.py         # Currency formatting utilities
│       ├── encoding_utils.py         # Encoding utilities
│       └── schema_validator.py       # JSON schema validation
├── tests/
│   ├── API/                          # API test cases
│   │   ├── test_create_account_with_invalid_from_account.py
│   │   ├── test_create_new_account.py
│   │   ├── test_fund_transfer_transaction_recording.py
│   │   ├── test_get_account_details.py
│   │   └── test_get_accounts_for_customer.py
│   └── UI/                           # UI test cases
│       ├── test_failed_login.py
│       ├── test_left_navigation_panel.py
│       ├── test_success_login.py
│       ├── test_transfer_funds.py
│       └── test_view_account_details.py
├── reports/                          # Test reports (auto-generated)
└── test-results/                     # Test artifacts (screenshots, traces)
   └── traces/
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
