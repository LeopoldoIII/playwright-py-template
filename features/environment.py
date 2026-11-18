"""
Behave lifecycle hooks managing Playwright Browser and API contexts.
"""
from typing import Any
from playwright.sync_api import sync_playwright

from config import HEADLESS, SLOW_MO, API_BASE_URL
from pages.login_page import LoginPage
from features.types import StepContext


def before_all(context: StepContext) -> None:
    """Initialize Playwright engine, browser instance, and HTTP API client."""
    context.playwright = sync_playwright().start()

    context.browser = context.playwright.chromium.launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO
    )

    # Built-in Playwright HTTP client for API testing (no requests or urllib required)
    context.api = context.playwright.request.new_context(base_url=API_BASE_URL)


def before_scenario(context: StepContext, scenario: Any) -> None:
    """Create isolated browser context and page per scenario for strict test isolation."""
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()
    context.login_page = LoginPage(context.page)


def after_scenario(context: StepContext, scenario: Any) -> None:
    """Capture screenshot on failure and tear down page and browser context."""
    if scenario.status == "failed":
        safe_name = scenario.name.replace(" ", "_").lower()
        context.page.screenshot(path=f"failed_{safe_name}.png")

    context.page.close()
    context.browser_context.close()


def after_all(context: StepContext) -> None:
    """Dispose API client and terminate browser engine."""
    if hasattr(context, "api"):
        context.api.dispose()
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "playwright"):
        context.playwright.stop()
