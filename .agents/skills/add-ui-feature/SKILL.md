---
name: add-ui-feature
description: >-
  Use this skill whenever adding a new UI testing feature, Page Object, Gherkin scenario, or step definition.
  Ensures adherence to Clean POM, strict context typing in StepContext, and Playwright web-first assertions.
---

# Add UI Feature Workflow

Follow this procedure to introduce a new UI feature into the project.

## Step 1: Create the Page Object
Create a new file in `pages/<feature_name>_page.py`:
1. Inherit from `BasePage` (`from pages.base_page import BasePage`).
2. Declare locators in `__init__` (e.g. `self.page.locator(...)` or `self.page.get_by_role(...)`).
3. Implement user action methods without assertions.
4. Expose `open(url: Optional[str] = None)` defaulting to `BASE_URL` from `config.py`.

Example:
```python
from typing import Optional
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from config import BASE_URL

class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title: Locator = page.locator(".title")
        self.item_list: Locator = page.locator(".inventory_item")

    def open(self, url: Optional[str] = None) -> None:
        self.goto(url if url is not None else f"{BASE_URL}/inventory.html")
```

## Step 2: Register in `features/types.py`
Add the new page to `StepContext` to prevent breaking IDE "Go to Definition":
```python
from pages.inventory_page import InventoryPage

class StepContext(Context):
    ...
    inventory_page: InventoryPage
```

## Step 3: Instantiate in `features/environment.py`
Inside `before_scenario`:
```python
from pages.inventory_page import InventoryPage

def before_scenario(context: StepContext, scenario: Any) -> None:
    ...
    context.inventory_page = InventoryPage(context.page)
```

## Step 4: Write Gherkin Feature
Add scenario in `features/<feature_name>.feature` using tags (e.g. `@ui @smoke`):
```gherkin
Feature: Inventory Management

  @ui @smoke
  Scenario: Display product catalog
    Given the user navigates to the login page
    When the user logs in with standard credentials
    Then the user should see the product inventory
```

## Step 5: Implement Step Definitions with `StepContext`
In `features/steps/<feature_name>_steps.py`:
```python
from behave import given, when, then
from playwright.sync_api import expect
from features.types import StepContext

@then('the user should see the product inventory')
def step_verify_inventory(context: StepContext) -> None:
    expect(context.inventory_page.title).to_be_visible()
    expect(context.inventory_page.title).to_have_text("Products")
```

## Step 6: Verify
Run compilation check and test suite:
```bash
python3 -m py_compile pages/*.py features/*.py features/steps/*.py
behave --tags=@ui
```
