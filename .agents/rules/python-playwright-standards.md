# Python & Playwright Quality Standards

## Language
- All code, docstrings, typing annotations, comments, and commit messages MUST be written in English.

## Page Object Model Rules
1. **Inherit from `BasePage`**:
   Every new page class in `pages/` must inherit from `pages.base_page.BasePage`.
2. **Strictly Decouple Assertions**:
   - Page Objects must only return values, perform actions, or expose Locators (`Locator`).
   - Page Objects must NEVER contain `expect(...)` assertions or boolean test validations.
   - Assertions belong exclusively in step definition functions (`features/steps/`).
3. **Lazy Locator Declaration**:
   Define locators in `__init__` using `self.page.locator(...)` or semantic helpers (`self.page.get_by_role`, etc.). Locators are lazy descriptions and do not query the DOM until an action is executed.
4. **Environment Defaults**:
   Navigation methods such as `open()` should default to configuration constants from `config.py` (e.g. `BASE_URL`), allowing optional override.

## UI Action & Assertion Rules
1. **Auto-Waiting**:
   Playwright automatically waits for actionable states (visible, stable, enabled, not obscured). Never introduce arbitrary `time.sleep()`.
2. **Action Methods**:
   - Use `.fill()` for instant form completion.
   - Use `.press_sequentially()` when testing autocomplete, keyboard listeners, or debounced inputs.
   - Use `.check()` and `.uncheck()` for checkboxes (idempotent).
   - Use `.hover()` for mouse-over states.
3. **Web-First Assertions**:
   Always assert locators using `expect(locator).to_...`:
   - `expect(locator).to_be_visible()`
   - `expect(locator).to_have_text(...)` / `to_contain_text(...)`
   - `expect(locator).to_be_enabled()` / `to_be_checked()`
   - `expect(page).to_have_url(...)`
