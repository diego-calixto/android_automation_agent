---
name: ui-automator-validation
description: Use when the task requires checking whether UI elements, tiles, or text exist or do not exist on the connected Android device.
---

# UiAutomator Validation Skill

This skill supports validation-focused tasks such as confirming the presence or absence of screens, tiles, icons, text, or app state.

## Use when

- The instruction asks to verify that something exists.
- The instruction asks to validate that something is missing.
- The user requests a check after navigation or interaction.

## Guidance

- Use `exists(xpath, timeout=...)` for presence checks.
- Use `find_element(xpath)` only when you need to inspect properties or interact with the element.
- For absence checks, confirm that `exists()` returns `False` and that the element is not visible.
- Return explicit, actionable output: what was checked, how it was checked, and the pass/fail result.

## Examples

- "check if Display settings exists" → verify a Settings entry labeled "Display".
- "verify if favorites tiles has an icon" → locate the favorites tile and confirm an icon is present in its subtree.
- "validate that there is no 'abracadabra' tiles" → search the quick settings tile list for "abracadabra" and confirm it is absent.
