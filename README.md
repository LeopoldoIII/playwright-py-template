# Minimal Playwright & Behave BDD Template (Python)

A production-ready, pure BDD test automation template engineered specifically for technical automation interviews, pair-programming sessions, and enterprise testing using Playwright, Behave (Gherkin), and Clean Page Object Model.

---

## 1. Quick Setup (Under 1 Minute)

Run the following commands in your terminal:

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Chromium browser binary
playwright install chromium
```

---

## 2. Test Execution Commands

### Running BDD Scenarios (Behave)
```bash
# Run all scenarios (UI + API)
behave

# Run UI scenarios only
behave --tags=@ui

# Run API scenarios only (runs in < 300ms)
behave --tags=@api

# Run negative test scenarios
behave --tags=@negative

# Run specific scenario by line number
behave features/smoke.feature:4
```

---

## 3. Project Structure

```
playwright-behave-template/
├── .env                         # Execution flags and credentials (not committed to VCS)
├── .env.example                 # Template for environment variables
├── config.py                    # Centralized typed configuration loaded via python-dotenv
├── requirements.txt             # Minimal dependencies (playwright, behave, python-dotenv)
├── .vscode/                     # Editor autocomplete for Gherkin and Python
│   ├── settings.json
│   └── extensions.json
├── pages/                       # Page Object Model layer
│   ├── base_page.py             # Action wrappers (click, fill, hover, type, select, check, wait)
│   └── login_page.py            # SauceDemo LoginPage object
└── features/                    # BDD / Cucumber Layer
    ├── environment.py           # Playwright browser lifecycle & native API client
    ├── types.py                 # Typed Behave Context enabling IDE autocompletion & navigation
    ├── smoke.feature            # UI + API scenarios
    └── steps/
        └── smoke_steps.py       # Step definitions with Web-First assertions
```

---

## 4. Key Interview Talking Points

### A. Playwright vs. Selenium: Core Architectural Differences

| Dimension | Selenium (WebDriver) | Playwright (sync_api) | Key Interview Takeaway |
| :--- | :--- | :--- | :--- |
| **Communication Protocol** | HTTP / JSON Wire / W3C WebDriver (request/response per action) | **WebSocket (persistent single connection)** | Playwright communicates directly with Chrome DevTools Protocol (CDP) and browser engines with almost zero network latency. |
| **Waiting Strategy** | Imperative polling via `WebDriverWait` + `expected_conditions` | **Built-in Auto-Waiting** | Playwright automatically checks element attachment, visibility, stability, and enablement before executing any action. |
| **Locators Evaluation** | Immediate (`find_element` queries DOM immediately; throws `NoSuchElementException`) | **Lazy Evaluation** | `page.locator(...)` is only a description. It doesn't query the DOM until an action (e.g., `.click()`) is invoked. |
| **Assertions** | Python standard `assert` or third-party hamcrest | **Web-First Assertions (`expect`)** | `expect(locator).to_have_text(...)` retries automatically until condition is met or timeout expires, eliminating race conditions. |
| **Native API Client** | None (requires `requests` or `urllib3`) | **Built-in (`request.new_context`)** | Unified cookies, headers, and authentication between API requests and UI browser sessions. |

---

### B. Indispensable UI Methods Cheat Sheet (Python)

In Playwright (`sync_api`), you first define the locator (`page.locator(...)` or semantic helpers like `page.get_by_role(...)`) and then execute the action:

| UI Action | Selenium (`webdriver`) | Playwright (`sync_api`) | Key Interview Notes |
| :--- | :--- | :--- | :--- |
| **Navigate to URL** | `driver.get("https://...")` | `page.goto("https://...")` | Playwright waits by default for the `load` event. |
| **Find Element** | `driver.find_element(By.CSS_SELECTOR, "...")` | `page.locator("...")` or `page.get_by_role(...)` | Playwright locators are **lazy** (they do not query the DOM until an action is executed). |
| **Click** | `element.click()` | `locator.click()` | Auto-waits for element to be visible, stable, receive events, and not be covered. |
| **Fill Input** | `element.clear()` + `element.send_keys("abc")` | `locator.fill("abc")` | `.fill()` clears the input and inserts text instantly. To simulate real human typing letter-by-letter, use `locator.press_sequentially("abc")`. |
| **Get Visible Text** | `element.text` | `locator.inner_text()` | `inner_text()` returns only rendered/visible text. `locator.text_content()` returns all node text (equivalent to `textContent`). |
| **Get Input Value** | `element.get_attribute("value")` | `locator.input_value()` | Playwright has a dedicated method exclusively for `<input>`, `<textarea>`, and `<select>` values. |
| **Get Attribute** | `element.get_attribute("href")` | `locator.get_attribute("href")` | Functions identically. |
| **Select Dropdown** | `Select(element).select_by_value("1")` | `locator.select_option("1")` | No need to import a separate `Select` class; accepts `value`, label (`label="Option"`), or `index`. |
| **Checkbox / Radio** | `if not element.is_selected(): element.click()` | `locator.check()` / `locator.uncheck()` | `.check()` is **idempotent**: if already checked, it performs no action. |
| **Hover** | `ActionChains(driver).move_to_element(el).perform()` | `locator.hover()` | No need to instantiate or chain action classes. |
| **Wait for Visibility** | `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))` | `locator.wait_for(state="visible")` | Rarely needed manually because actions auto-wait automatically. |
| **Assertions (Validate)** | `assert "Hello" in element.text` | `expect(locator).to_have_text("Hello")` | `expect()` retries automatically with a configurable timeout until the assertion passes. |

---

### C. Strategic Interview Q&A

#### 1. Why create wrappers in `BasePage` if Playwright already handles auto-waiting?
1. **Centralized Logging & Failure Telemetry**: A single location to attach step screenshots, metrics, or custom failure traces across all test steps.
2. **Locator Flexibility (`_get_locator`)**: Allows methods to accept both modern Playwright semantic locators (`page.get_by_role(...)`) and legacy string selectors (`CSS/XPath`) seamlessly without refactoring method signatures.
3. **Controlled Global Timeouts**: Define consistent timeout policies across the entire test suite without repeating parameters in every test script.

#### 2. Why are assertions intentionally excluded from `BasePage`? (Clean POM)
- **Single Responsibility Principle (SRP)**: Page Objects represent the **state of the UI** and provide services to interact with it; test cases or step definitions represent the **business requirements** and verify outcomes.
- **Reusability & Flexibility**: If a Page Object contains hardcoded assertions, the same UI action cannot be reused in negative scenarios or alternative verification flows.
- **Clean Failure Reporting**: When an assertion fails, the test report points directly to the test or scenario step rather than burying the failure inside an internal page helper.
