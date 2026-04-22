---
name: android-settings-map
description: Navigate and interact with Android Settings app by section and keywords
---

# Android Settings Map Skill

Use this skill to locate and navigate Android Settings sections. When given a settings goal, identify the relevant section and use its keywords to find the UI element.

## How to Use

1. **Identify the target section** from the map below based on the user's goal
2. **Use the section keywords** to construct XPath locators or UI searches
3. **Prefer exact matches** over contains matches when possible
4. **Always verify** with UI hierarchy inspection before interacting
5. **Scroll if needed** to find elements outside viewport

## Android Settings Sections

| Section | Target | Keywords |
|---------|--------|----------|
| **Network & Internet** | Mobile networking, Wi-Fi, hotspot | Network, Internet, Wi-Fi, Mobile, Hotspot, SIM |
| **Connected Devices** | Bluetooth, paired devices | Connected, Bluetooth, Pair, Device |
| **Apps** | Application management, permissions | Apps, App info, Permissions |
| **Notifications** | Alerts, Do Not Disturb | Notifications, Alerts, Do Not Disturb |
| **Battery** | Power management, usage | Battery, Power, Usage, Saver |
| **Display** | Screen settings, brightness | Display, Brightness, Dark, Screen, Timeout, Adaptive brightness |
| **Sound** | Volume, vibration | Sound, Volume, Vibration |
| **Storage** | Device storage, files | Storage, Files, Space |
| **Security & Privacy** | Lock screen, fingerprint, permissions, camera, microphone | Security, Lock, Fingerprint, Face, Encryption, Privacy, Permissions, Camera, Microphone |
| **Location** | GPS, location settings | Location, GPS |
| **Safety & Emergency** | Emergency features, SOS | Safety, Emergency, SOS |
| **Passwords & Accounts** | Account sync, authentication | Passwords, Accounts, Google, Sync |
| **Digital Wellbeing** | Screen time, focus mode | Wellbeing, Screen time, Focus mode, Parental |
| **Google** | Google services | Google, Services |
| **Accessibility** | Vision, hearing aids, TalkBack | Accessibility, TalkBack, Vision, Hearing |
| **System** | Date, language, gestures, reset | System, Languages, Gestures, Backup, Reset, Date |
| **About Phone** | Version, build info | About, Phone, Build, Version, Android version |

## Locator Strategy

1. **Try exact text match**: `//*[@text='Network & Internet']`
2. **Fall back to partial match**: `//*[contains(@text, 'Network')]`
3. **Use content-desc if text fails**: `//*[contains(@content-desc, 'network')]`

## Important Notes

- Always run `dump_hierarchy` first before constructing locators
- ScrollView lists are scrollable—swipe down to find items not in viewport
- Prefer clickable elements; avoid using index-based locators
- Settings structure is consistent across Android versions
- Keywords are redundant for robustness—use the closest match