"""
Type annotations for Behave Context.

Provides static type hints for dynamic attributes attached during the Behave
lifecycle (Playwright browser, contexts, pages, and Page Objects) to enable
full IDE autocompletion, type checking, and 'Go to Definition' (F12 / Cmd+Click).
"""
from behave.runner import Context
from playwright.sync_api import (
    Page,
    Playwright,
    Browser,
    BrowserContext,
    APIRequestContext,
    APIResponse,
)
from pages.login_page import LoginPage


class StepContext(Context):
    """
    Typed context representation for Behave step definitions and hooks.

    Extends behave.runner.Context with typed definitions of all runtime
    attributes created in before_all and before_scenario.
    """
    playwright: Playwright
    browser: Browser
    browser_context: BrowserContext
    page: Page
    login_page: LoginPage
    api: APIRequestContext
    api_response: APIResponse
