# Step Definition Typing & Navigation Rules

## Core Rule: Never Break IDE "Go to Definition"
Because Behave attaches objects to `context` dynamically at runtime, untyped contexts (`context: Any`) prevent IDEs (VS Code Pylance, Pyright, PyCharm) from resolving method definitions or providing IntelliSense.

## Mandatory Practices

### 1. Mandatory `StepContext` Parameter Type
Every step definition in `features/steps/*.py` and hook in `features/environment.py` MUST import and annotate the `context` parameter using `StepContext`:
```python
from features.types import StepContext

@given('...')
def step_impl(context: StepContext) -> None:
    ...
```
**`context: Any` is strictly forbidden.**

### 2. Synchronize `features/types.py` When Modifying `context`
Whenever you instantiate and attach a new Page Object, service, or API attribute in `features/environment.py` (e.g. `context.checkout_page = CheckoutPage(context.page)`):
1. Open [features/types.py](file:///Users/usermone/local/projects/py/playwright-py-template/features/types.py).
2. Import the newly created Page Object class.
3. Add the attribute type declaration to `StepContext`:
```python
class StepContext(Context):
    # Existing attributes
    page: Page
    login_page: LoginPage
    # NEW attribute must be declared here:
    checkout_page: CheckoutPage
```

### 3. Verification
Verify that `python3 -m py_compile features/types.py features/environment.py features/steps/*.py` passes with zero errors after any modification.
