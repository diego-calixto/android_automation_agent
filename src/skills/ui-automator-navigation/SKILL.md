---
name: ui-automator-navigation
description: Use when translating natural language navigation steps into Android UiAutomator actions such as launching apps, opening settings, and navigating screens.
---

# UiAutomator Navigation Skill

This skill helps the agent convert broad instructions like "open settings" or "go to quick settings" into concrete device actions.

## Use when

- The user asks to open an app, system screen, or device panel.
- The instruction references navigation, menus, settings, or app launch.
- The agent must select a path to reach the target screen.

## Guidance

- Prefer `launch_app(package_name, activity=None)` when a package is known or obvious.
- Use `press_home()` and UI clicks when entering a screen through the visible UI is safer.
- For system panels like quick settings, use available device commands or shell actions if direct UI clicks are not stable.
- If the target is in Settings, identify the Settings package and locate the expected list entry.

## Examples

- "Go to settings" → `launch_app("com.android.settings")`
- "Open files app" → `launch_app("com.android.documentsui")` or a known file manager package
- "Open quick settings" → use device navigation or panel command if available
