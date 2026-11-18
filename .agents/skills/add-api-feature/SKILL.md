---
name: add-api-feature
description: >-
  Use this skill whenever adding a new API testing scenario or endpoint verification using Playwright's native HTTP client.
  Covers request configuration, payload handling, status validation, and schema verification.
---

# Add API Feature Workflow

Follow this procedure to introduce a new REST API scenario using Playwright's native APIRequestContext.

## Step 1: Ensure API Configuration in `config.py`
Verify that the target API endpoint base URL is defined in `config.py` and `.env` (`API_BASE_URL`).

## Step 2: Define Gherkin Scenarios
In `features/api_<feature_name>.feature` or existing feature file:
```gherkin
Feature: API User Service

  @api @smoke
  Scenario: Fetch user profile by ID
    When the user requests API details for user "2"
    Then the API response status code should be 200
    And the response body should contain username "michaelw"
```

## Step 3: Implement Step Definitions using `StepContext`
In `features/steps/api_steps.py` (or existing step file):
```python
from behave import when, then
from features.types import StepContext

@when('the user requests API details for user "{user_id}"')
def step_get_user(context: StepContext, user_id: str) -> None:
    # Uses native Playwright HTTP context from environment.py
    context.api_response = context.api.get(f"/users/{user_id}")

@then('the API response status code should be {status_code:d}')
def step_verify_status(context: StepContext, status_code: int) -> None:
    assert context.api_response.status == status_code, (
        f"Expected status {status_code}, got {context.api_response.status}"
    )

@then('the response body should contain username "{expected_username}"')
def step_verify_username(context: StepContext, expected_username: str) -> None:
    data = context.api_response.json()
    assert data.get("username") == expected_username
```

## Step 4: Verify
Run compilation check and execute API tags:
```bash
python3 -m py_compile features/steps/*.py
behave --tags=@api
```
