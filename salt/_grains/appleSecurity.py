import os
import re
import plistlib
import subprocess


XPROTECT_BINARY = "/usr/bin/xprotect"

XPROTECT_REMEDIATOR_PLIST = (
    "/Library/Apple/System/Library/CoreServices/"
    "XProtect.app/Contents/Info.plist"
)


def _run_command(command):
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except Exception:
        return None


def _get_gatekeeper():
    output = _run_command([
        "/usr/sbin/spctl",
        "--status"
    ])

    if not output:
        return {
            "enabled": None
        }

    return {
        "enabled": "enabled" in output.lower()
    }


def _get_firewall():
    output = _run_command([
        "/usr/libexec/ApplicationFirewall/socketfilterfw",
        "--getglobalstate"
    ])

    if not output:
        return {
            "enabled": None
        }

    return {
        "enabled": (
            "Firewall is enabled" in output
        )
    }


def _get_sip():
    output = _run_command([
        "/usr/bin/csrutil",
        "status"
    ])

    if not output:
        return {
            "enabled": None
        }

    return {
        "enabled": (
            "System Integrity Protection status: enabled"
            in output
        )
    }


def _get_filevault():
    output = _run_command([
        "/usr/bin/fdesetup",
        "status"
    ])

    if not output:
        return {
            "enabled": None
        }

    return {
        "enabled": (
            "FileVault is On" in output
        )
    }


def _get_xprotect():
    data = {
        "version": None,
        "installed": None,
        "latestAvailableVersion": None,
        "updatePublished": None,
        "updateAvailable": False
    }

    version_output = _run_command([
        XPROTECT_BINARY,
        "version"
    ])

    if version_output:
        match = re.search(
            r"Version:\s+(\S+)\s+Installed:\s+(.+)$",
            version_output
        )

        if match:
            data["version"] = match.group(1)
            data["installed"] = match.group(2)

    check_output = _run_command([
        XPROTECT_BINARY,
        "check"
    ])

    if check_output:
        match = re.search(
            r"Current update:\s+date:\s+(.+?)\s+version:\s+(\S+)",
            check_output
        )

        if match:
            data["updatePublished"] = match.group(1)
            data["latestAvailableVersion"] = match.group(2)

    if (
        data["version"]
        and data["latestAvailableVersion"]
        and data["version"] != data["latestAvailableVersion"]
    ):
        data["updateAvailable"] = True

    return data


def _get_xprotect_remediator():
    data = {
        "version": None
    }

    if not os.path.exists(XPROTECT_REMEDIATOR_PLIST):
        return data

    try:
        with open(XPROTECT_REMEDIATOR_PLIST, "rb") as plist_file:
            plist_data = plistlib.load(plist_file)

        data["version"] = plist_data.get(
            "CFBundleShortVersionString"
        )

    except Exception:
        pass

    return data


def appleSecurity():
    return {
        "appleSecurity": {
            "gatekeeper": _get_gatekeeper(),
            "firewall": _get_firewall(),
            "sip": _get_sip(),
            "filevault": _get_filevault(),
            "xprotect": _get_xprotect(),
            "xprotectRemediator": _get_xprotect_remediator()
        }
    }
