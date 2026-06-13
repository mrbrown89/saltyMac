# Apple Security Salt Grain

Custom Salt grain for collecting Apple security posture information from macOS devices.

## Overview

`appleSecurity.py` is a custom Salt grain that provides a consolidated view of key macOS security technologies.

The grain is designed for:

- Health check reporting
- Security posture validation
- Fleet visibility
- Compliance reporting
- Troubleshooting
- Future Salt targeting

The grain intentionally returns lightweight security metadata only and does not modify device state.

---

## Location

```text
salt/_grains/appleSecurity.py
```

---

## Purpose

The grain provides a reusable, structured way to understand:

- Whether Gatekeeper is enabled
- Whether the macOS Firewall is enabled
- Whether System Integrity Protection (SIP) is enabled
- Whether FileVault is enabled
- Installed XProtect version
- Available XProtect version
- XProtect publication date
- XProtect Remediator version

This allows Salty Macs health checks and Salt targeting to consume a single source of truth for Apple security controls.

---

## Grain Name

```yaml
appleSecurity
```

---

## Example Grain Output

```yaml
appleSecurity:
  gatekeeper:
    enabled: true

  firewall:
    enabled: true

  sip:
    enabled: true

  filevault:
    enabled: true

  xprotect:
    version: "5347"
    installed: "2026-06-03 01:43:47 +0000"
    latestAvailableVersion: "5347"
    updatePublished: "2026-06-02 21:39:16 +0000"
    updateAvailable: false

  xprotectRemediator:
    version: "157"
```

---

## Current Fields

### Gatekeeper

```yaml
gatekeeper:
  enabled: true
```

| Field | Description |
|---------|---------|
| `enabled` | Whether Gatekeeper assessments are enabled |

---

### Firewall

```yaml
firewall:
  enabled: true
```

| Field | Description |
|---------|---------|
| `enabled` | Whether the macOS Application Firewall is enabled |

---

### SIP

```yaml
sip:
  enabled: true
```

| Field | Description |
|---------|---------|
| `enabled` | Whether System Integrity Protection is enabled |

---

### FileVault

```yaml
filevault:
  enabled: true
```

| Field | Description |
|---------|---------|
| `enabled` | Whether FileVault disk encryption is enabled |

---

### XProtect

```yaml
xprotect:
  version: "5347"
  installed: "2026-06-03 01:43:47 +0000"
  latestAvailableVersion: "5347"
  updatePublished: "2026-06-02 21:39:16 +0000"
  updateAvailable: false
```

| Field | Description |
|---------|---------|
| `version` | Installed XProtect version |
| `installed` | Date and time the current XProtect version was installed |
| `latestAvailableVersion` | Latest XProtect version currently available from Apple |
| `updatePublished` | Publication timestamp of the latest available XProtect update |
| `updateAvailable` | Whether the installed version differs from the latest available version |

---

### XProtect Remediator

```yaml
xprotectRemediator:
  version: "157"
```

| Field | Description |
|---------|---------|
| `version` | XProtect Remediator version derived from the XProtect application bundle |

---

## Getting Grain Data

### Get Full Apple Security Grain

```bash
salt 'macbook01' grains.get appleSecurity
```

### Get Gatekeeper Status

```bash
salt 'macbook01' grains.get appleSecurity:gatekeeper:enabled
```

### Get Firewall Status

```bash
salt 'macbook01' grains.get appleSecurity:firewall:enabled
```

### Get SIP Status

```bash
salt 'macbook01' grains.get appleSecurity:sip:enabled
```

### Get FileVault Status

```bash
salt 'macbook01' grains.get appleSecurity:filevault:enabled
```

### Get XProtect Version

```bash
salt 'macbook01' grains.get appleSecurity:xprotect:version
```

### Check Whether an XProtect Update Is Available

```bash
salt 'macbook01' grains.get appleSecurity:xprotect:updateAvailable
```

### Get XProtect Remediator Version

```bash
salt 'macbook01' grains.get appleSecurity:xprotectRemediator:version
```

---

## Example Usage in States

### Run State Only When FileVault Is Enabled

```jinja
{% if grains['appleSecurity']['filevault']['enabled'] %}

filevault-enabled:
  test.show_notification:
    - text: "FileVault is enabled"

{% endif %}
```

### Alert When XProtect Is Out Of Date

```jinja
{% if grains['appleSecurity']['xprotect']['updateAvailable'] %}

xprotect-update-required:
  test.show_notification:
    - text: >
        XProtect update available:
        {{ grains['appleSecurity']['xprotect']['version'] }}
        ->
        {{ grains['appleSecurity']['xprotect']['latestAvailableVersion'] }}

{% endif %}
```

### Alert When SIP Is Disabled

```jinja
{% if not grains['appleSecurity']['sip']['enabled'] %}

sip-disabled:
  test.show_notification:
    - text: "System Integrity Protection is disabled"

{% endif %}
```

---

## Data Sources

### Gatekeeper

Collected using:

```bash
spctl --status
```

Example output:

```text
assessments enabled
```

---

### Firewall

Collected using:

```bash
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

Example output:

```text
Firewall is enabled. (State = 1)
```

---

### System Integrity Protection (SIP)

Collected using:

```bash
csrutil status
```

Example output:

```text
System Integrity Protection status: enabled.
```

---

### FileVault

Collected using:

```bash
fdesetup status
```

Example output:

```text
FileVault is On.
```

---

### XProtect

Installed version information is collected using:

```bash
xprotect version
```

Example output:

```text
Version: 5347 Installed: 2026-06-03 01:43:47 +0000
```

Latest available update information is collected using:

```bash
xprotect check
```

Example output:

```text
Current update: date: 2026-06-02 21:39:16 +0000 version: 5347
```

---

### XProtect Remediator

Version information is collected from:

```text
/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/Info.plist
```

Specifically:

```text
CFBundleShortVersionString
```

---

## Health Check Integration

The grain is designed to support the Salty Macs Health Check.

Example output:

```text
Apple Security
----------------------------------------
[OK]    Gatekeeper enabled
[OK]    Firewall enabled
[OK]    SIP enabled
[OK]    FileVault enabled
[OK]    XProtect version: 5347
[OK]    XProtect is current
[OK]    XProtect Remediator version: 157
```

---

## Design Principles

The grain intentionally:

- Uses native macOS security tooling
- Avoids MDM API usage
- Avoids network calls
- Avoids external dependencies
- Returns lightweight metadata only
- Provides device-level security posture information
- Fails safely when data cannot be collected

---

## Notes

- Gatekeeper, SIP, Firewall, and FileVault are device-level security controls.
- XProtect updates are delivered independently of macOS upgrades.
- XProtect publication dates are reported directly by Apple's `xprotect` utility.
- XProtect installation dates indicate when the current version was installed on the device.
- XProtect Remediator version information is obtained from the XProtect application bundle metadata.
- The grain is read-only and performs no configuration changes.
