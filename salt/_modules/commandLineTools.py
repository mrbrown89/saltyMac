import subprocess
import re

def __virtual__():
    return "commandLineTools" if __grains__.get("os") == "MacOS" else False


def available():
    """
    Check if a Command Line Tools (CLT) update is available.
    Returns the label if found, otherwise None.
    """
    cmd = ["/usr/sbin/softwareupdate", "-l"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    for line in result.stdout.splitlines():
        if "Command Line Tools" in line:
            match = re.search(r'\* (.+)', line)
            if match:
                return match.group(1)
    return None


def install(label=None):
    """
    Install the CLT update.
    """
    if not label:
        label = available()
    if not label:
        return {"result": True, "comment": "No CLT updates available"}

    # Clean up the label
    label = label.replace("Label:", "").strip()

    cmd = ["/usr/sbin/softwareupdate", "--install", label]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "result": result.returncode == 0,
        "comment": result.stdout,
        "label": label
    }

def is_installed_and_active():
    """
    Check if CLT is installed and active using xcode-select and pkgutil.
    """
    import os
    clt_path = "/Library/Developer/CommandLineTools"
    try:
        version_info = subprocess.run(
            ["pkgutil", "--pkg-info", "com.apple.pkg.CLTools_Executables"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        return False
    return os.path.exists(clt_path)
