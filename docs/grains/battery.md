# macOS Battery Salt Grain

Custom Salt grain for collecting battery information from macOS devices.

## Overview

This grain provides basic battery health and charging information for macOS systems.

The grain returns:

- Whether a battery is present
- Device type (desktop or laptop)
- Battery condition
- Cycle count
- Maximum battery capacity percentage
- Charging status
- Current power source

---

## Grain Name

```yaml
battery
```

---

## Example Grain Output

### Laptop Example

```yaml
battery:
  present: true
  device_type: laptop
  condition: Normal
  cycle_count: 182
  maximum_capacity_percent: 91
  charging: true
  power_source: AC Power
```

### Desktop Example

```yaml
battery:
  present: false
  device_type: desktop
```

---

## Getting Grain Data

### Get Full Battery Grain

```bash
salt 'macbook01' grains.get battery
```

### Get Battery Condition

```bash
salt 'macbook01' grains.get battery:condition
```

### Get Cycle Count

```bash
salt 'macbook01' grains.get battery:cycle_count
```

### Get Maximum Capacity Percentage

```bash
salt 'macbook01' grains.get battery:maximum_capacity_percent
```

### Check If Device Is Charging

```bash
salt 'macbook01' grains.get battery:charging
```

### Get Current Power Source

```bash
salt 'macbook01' grains.get battery:power_source
```

### Check Device Type

```bash
salt 'macbook01' grains.get battery:device_type
```

---

## Example Usage in States

### Run State Only on Laptops

```jinja
{% if grains['battery']['device_type'] == 'laptop' %}

install-laptop-software:
  pkg.installed:
    - name: zoom

{% endif %}
```

### Alert on Low Battery Health

```jinja
{% if grains['battery'].get('maximum_capacity_percent', 100) < 80 %}

battery-health-warning:
  test.show_notification:
    - text: "Battery health below 80%"

{% endif %}
```

### Check Charging Status

```jinja
{% if grains['battery'].get('charging') %}

charging-message:
  test.show_notification:
    - text: "Device is charging"

{% endif %}
```

---

## Data Sources

This grain uses the following macOS commands:

### system_profiler

Used for:

- Battery condition
- Cycle count
- Maximum capacity

### pmset

Used for:

- Charging status
- Power source

---

## Notes

- Desktop Macs return:

```yaml
present: false
device_type: desktop
```

