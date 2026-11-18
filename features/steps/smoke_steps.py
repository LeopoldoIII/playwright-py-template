"""
Step definitions covering UI (SauceDemo) and API (REST) scenarios.
"""
import re
from behave import given, when, then
from playwright.sync_api import expect
from features.types import StepContext


# ==========================================
# UI Step Definitions
# ==========================================

@given('the user navigates to the login page')
def step_navigate_login(context: StepContext) -> None:
    """Navigate to the target login page."""
    context.login_page.open()


@when('the user logs in with username "{username}" and password "{password}"')
def step_login_credentials(context: StepContext, username: str, password: str) -> None:
    """Submit credentials on the login page."""
    context.login_page.login(username, password)


@then('the user should see the inventory page header')
def step_verify_inventory_page(context: StepContext) -> None:
    """Verify redirection to inventory and visible products title."""
    # Web-first URL assertion (automatically retries until navigation finishes)
    expect(context.page).to_have_url(re.compile(r".*inventory\.html"))

    # Web-first Locator assertion
    header = context.page.locator(".title")
    expect(header).to_be_visible()
    expect(header).to_have_text("Products")


@then('the user should see the error message "{expected_message}"')
def step_verify_login_error(context: StepContext, expected_message: str) -> None:
    """Verify error banner visibility and text content."""
    error_banner = context.login_page.error_message
    expect(error_banner).to_be_visible()
    expect(error_banner).to_contain_text(expected_message)


# ==========================================
# API Step Definitions (Native Playwright HTTP)
# ==========================================

@when('the user requests API details for user "{user_id}"')
def step_api_get_user(context: StepContext, user_id: str) -> None:
    """Execute GET request using Playwright's native HTTP context."""
    context.api_response = context.api.get(f"/users/{user_id}")


@when('the user creates a new user with firstName "{first_name}" and lastName "{last_name}"')
def step_api_create_user(context: StepContext, first_name: str, last_name: str) -> None:
    """Execute POST request with JSON payload using Playwright's native HTTP context."""
    payload = {
        "firstName": first_name,
        "lastName": last_name
    }
    context.api_response = context.api.post(
        "/users/add",
        data=payload,
        headers={"Content-Type": "application/json"}
    )


@then('the API response status code should be {status_code:d}')
def step_verify_api_status(context: StepContext, status_code: int) -> None:
    """Verify HTTP response status code."""
    actual_status = context.api_response.status
    assert actual_status == status_code, (
        f"Expected HTTP status {status_code}, but got {actual_status}."
    )


@then('the response body should contain username "{expected_username}"')
def step_verify_api_username(context: StepContext, expected_username: str) -> None:
    """Verify username attribute in the response body."""
    data = context.api_response.json()
    actual_username = data.get("username")
    assert actual_username == expected_username, (
        f"Expected username '{expected_username}', got '{actual_username}'."
    )


@then('the response body should contain firstName "{expected_first_name}"')
def step_verify_api_firstname(context: StepContext, expected_first_name: str) -> None:
    """Verify firstName attribute in the response body."""
    data = context.api_response.json()
    actual_name = data.get("firstName")
    assert actual_name == expected_first_name, (
        f"Expected firstName '{expected_first_name}', got '{actual_name}'."
    )
