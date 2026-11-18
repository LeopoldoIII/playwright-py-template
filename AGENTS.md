# Antigravity AI Project Rules & Guidelines

## 1. Universal Language Requirement
- **All code, docstrings, comments, test descriptions, Gherkin scenarios, and technical documentation MUST be written strictly in English.**
- When interacting with the user, respond in the user's preferred language, but ensure that all repository assets (code, git messages, docs) remain 100% in English.

---

## 2. Core Python & Playwright Standards

### Page Object Model (Clean POM)
- **Separation of Concerns**: Page Objects in `pages/` represent UI state, locators, and user interactions.
- **NO Assertions in Page Objects**: Do not import or execute `expect(...)` inside Page Objects. Assertions belong strictly in step definitions (`features/steps/`).
- **Inheritance**: All Page Objects must inherit from `BasePage` (`pages.base_page.BasePage`).
- **Locators**: Use `page.locator(...)` or semantic locators (`page.get_by_role`, `page.get_by_label`, `page.get_by_test_id`). Locators are lazy; declare them in `__init__`.

### Web-First Assertions
- In step definitions, always prefer Playwright's web-first assertions (`expect(locator).to_be_visible()`, `expect(locator).to_have_text(...)`, `expect(page).to_have_url(...)`).
- Do NOT use manual polling, `time.sleep()`, or raw Python `assert locator.inner_text() == ...` for UI states, as Playwright's auto-waiting handles stability automatically.

### Centralized Configuration
- Never hardcode URLs, credentials, timeouts, or execution flags.
- Always import settings from `config.py` (e.g. `BASE_URL`, `API_BASE_URL`, `STANDARD_USER`, `SECRET_PASSWORD`, `DEFAULT_TIMEOUT`, `HEADLESS`, `SLOW_MO`).
- Any new environment variable must be defined in `config.py`, `.env`, and `.env.example`.

---

## 3. Strict Step Definition Typing (Prevent Broken IDE Navigation)

To prevent breaking "Go to Definition" (F12 / Cmd+Click) and IDE autocomplete in VS Code and PyCharm:
- **NEVER use `context: Any` in step definitions.**
- **ALWAYS type the context parameter as `StepContext`** (`from features.types import StepContext`).
- **Synchronize `features/types.py`**: When creating a new Page Object or attaching any new attribute to `context` (in `before_scenario` or `before_all` in `features/environment.py`), you **MUST** immediately declare the attribute and its type in `StepContext` within `features/types.py`.

Example:
```python
# features/steps/my_steps.py
from behave import given, when, then
from features.types import StepContext

@given('the user is on the dashboard')
def step_dashboard(context: StepContext) -> None:
    context.dashboard_page.open()  # Resolves with full IntelliSense and Go-to-Definition
```

---

## 4. Skills Directory
Specialized procedural workflows for this project are located in:
- `.agents/skills/add-ui-feature/`: Step-by-step workflow for creating UI pages, steps, and scenarios.
- `.agents/skills/add-api-feature/`: Step-by-step workflow for creating API tests with Playwright.
