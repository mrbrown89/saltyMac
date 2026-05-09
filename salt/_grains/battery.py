#!/usr/bin/env python3

'''
Salt grain: battery information for macOS

Provides:
    battery:
        present
        condition
        cycle_count
        maximum_capacity_percent
        charging
        power_source
'''

import subprocess
import re


def _run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def battery():
    '''
    Return battery information for macOS systems.
    '''

    grain = {
        'present': False,
        'device_type': 'desktop'
    }

    profiler_output = _run("system_profiler SPPowerDataType")

    # No battery detected
    if "Battery Information" not in profiler_output:
        return {'battery': grain}

    grain['present'] = True
    grain['device_type'] = 'laptop'

    # Condition
    condition_match = re.search(
        r'Condition:\s+(.+)',
        profiler_output
    )

    if condition_match:
        grain['condition'] = condition_match.group(1).strip()

    # Cycle Count
    cycle_match = re.search(
        r'Cycle Count:\s+(\d+)',
        profiler_output
    )

    if cycle_match:
        grain['cycle_count'] = int(cycle_match.group(1))

    # Maximum Capacity
    capacity_match = re.search(
        r'Maximum Capacity:\s+(\d+)%',
        profiler_output
    )

    if capacity_match:
        grain['maximum_capacity_percent'] = int(
            capacity_match.group(1)
        )

    # Charging / Power Source
    batt_output = _run("pmset -g batt")

    if "AC Power" in batt_output:
        grain['power_source'] = 'AC Power'
    elif "Battery Power" in batt_output:
        grain['power_source'] = 'Battery Power'

    grain['charging'] = "charging" in batt_output.lower()

    return {'battery': grain}
