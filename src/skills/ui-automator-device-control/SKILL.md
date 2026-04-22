---
name: ui-automator-device-control
description: Use when controlling the Android device state, apps, screen gestures, or device commands with UiAutomatorTools.
---

# UiAutomator Device Control Skill

This skill documents how to interact with the device reliably using the toolset available in `v2/uiautomator.py`.

## Use when

- The user wants clicks, swipes, scrolling, text entry, key presses, or shell commands.
- The agent must move between screens or manipulate app UI.

## Guidance

- Use `click(xpath, timeout=...)` for tappable elements.
- Use `long_click(xpath, timeout=..., duration=...)` for context menus or long-press actions.
- Use `set_text(xpath, text=...)` to fill input fields, clearing first if necessary.
- Use `scroll(xpath, direction=..., max_swipes=...)` or `swipe(start, end, duration=...)` for scrolling.
- Use `press_key(key)` and `press_back()` for device navigation and recovery.
- Reserve `execute_shell(command)` for device-level commands that cannot be completed through the UI.

## Examples

- "Tap the Display option" → `click(xpath=...)`
- "Scroll down in Settings" → `scroll(xpath=..., direction="down")`
- "Press back until the home screen appears" → `press_back()` repeatedly with checks.
