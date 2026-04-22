---
name: ui-automator-error-handling
description: Use when the agent should handle missing elements, ambiguous UI state, or recovery steps during Android automation.
---

# UiAutomator Error Handling Skill

This skill guides the agent on how to behave when UI elements are not found, validations fail, or the device state is uncertain.

## Use when

- An element cannot be located within timeout.
- The requested screen or app is not available.
- A validation fails and the agent must report a clear result.

## Guidance

- If `find_element()` fails, capture the attempted selector and report why the step failed.
- Do not continue executing unrelated actions after a critical failure.
- Ask for clarification when the user request is ambiguous or when multiple UI targets are possible.
- Prefer non-destructive recovery: use `press_back()` or `press_home()` before retrying.
- Use `screenshot()` if it will help diagnose why the UI lookup failed.

## Examples

- "Could not find Display settings after opening Settings" → report failure and include the xpath or text searched.
- "Tile missing during validation" → verify absence explicitly and avoid assuming the tile exists.
- "Unknown app package" → attempt heuristic launch but ask for the exact package if needed.
