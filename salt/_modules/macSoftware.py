import os
import plistlib
import subprocess

import salt.utils.platform


_DEFAULT_INSTALLOMATOR_PATH = "/usr/local/Installomator.zsh"


def __virtual__():
    if salt.utils.platform.is_darwin():
        return "macSoftware"
    return (False, "The macSoftware module only works on macOS")


def _run(cmd):
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 15 seconds", 1
    except OSError as exc:
        return "", str(exc), 1


def _readPlist(appPath):
    plistPath = os.path.join(appPath, "Contents", "Info.plist")

    if not os.path.exists(plistPath):
        return {}

    try:
        with open(plistPath, "rb") as plistFile:
            return plistlib.load(plistFile)
    except Exception:
        return {}


def _getSignatureInfo(appPath):
    stdout, stderr, retcode = _run(
        ["/usr/bin/codesign", "-dv", "--verbose=4", appPath]
    )

    output = "\n".join([stdout, stderr])

    info = {
        "signed": retcode == 0,
        "teamId": None,
        "authority": [],
        "identifier": None,
    }

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("TeamIdentifier="):
            info["teamId"] = line.split("=", 1)[1]

        elif line.startswith("Authority="):
            info["authority"].append(line.split("=", 1)[1])

        elif line.startswith("Identifier="):
            info["identifier"] = line.split("=", 1)[1]

    info["raw"] = output
    return info


def _getSpctlInfo(appPath):
    stdout, stderr, retcode = _run(
        ["/usr/sbin/spctl", "--assess", "--type", "execute", "--verbose=4", appPath]
    )

    output = "\n".join([stdout, stderr])

    return {
        "accepted": retcode == 0,
        "assessment": output,
    }


def _iterAppBundles(searchPaths=None, includeUserApplications=True):
    if searchPaths is None:
        searchPaths = [
            "/Applications",
            "/System/Applications",
            "/System/Applications/Utilities",
        ]

        if includeUserApplications:
            usersPath = "/Users"
            if os.path.exists(usersPath):
                for username in os.listdir(usersPath):
                    userApps = os.path.join(usersPath, username, "Applications")
                    if os.path.isdir(userApps):
                        searchPaths.append(userApps)

    seen = set()

    for rootPath in searchPaths:
        if not os.path.isdir(rootPath):
            continue

        for root, dirs, files in os.walk(rootPath):
            for dirname in list(dirs):
                if dirname.endswith(".app"):
                    appPath = os.path.join(root, dirname)

                    if appPath not in seen:
                        seen.add(appPath)
                        yield appPath

                    dirs.remove(dirname)


def _matches(value, pattern, exact=False):
    if value is None or pattern is None:
        return False

    valueLower = str(value).strip().lower()
    patternLower = str(pattern).strip().lower()

    if exact:
        return valueLower == patternLower

    return patternLower in valueLower


def _versionKey(version):
    parts = []

    for part in version.replace("-", ".").split("."):
        if part.isdecimal():
            parts.append((1, int(part)))
        else:
            parts.append((0, part.lower()))

    return tuple(parts)


def _highestDisplayVersion(apps):
    versions = [
        str(app["displayVersion"]).strip()
        for app in apps
        if app.get("displayVersion")
    ]

    return max(
        (version for version in versions if version),
        key=_versionKey,
        default=None,
    )


def getInstalledApps(
    name=None,
    exact=False,
    bundleId=None,
    teamId=None,
    includeSignature=True,
    includeGatekeeper=False,
    includeUserApplications=True,
    searchPaths=None,
):
    matches = []

    for appPath in _iterAppBundles(
        searchPaths=searchPaths,
        includeUserApplications=includeUserApplications,
    ):
        plist = _readPlist(appPath)
        bundleName = os.path.splitext(os.path.basename(appPath))[0]
        appNames = (
            plist.get("CFBundleDisplayName"),
            plist.get("CFBundleName"),
            bundleName,
        )
        displayName = appNames[0] or appNames[1] or bundleName

        bundleIdentifier = plist.get("CFBundleIdentifier")
        shortVersion = plist.get("CFBundleShortVersionString")
        buildVersion = plist.get("CFBundleVersion")

        if name and not any(
            _matches(appName, name, exact=exact) for appName in appNames
        ):
            continue

        if bundleId and not _matches(bundleIdentifier, bundleId, exact=exact):
            continue

        signatureInfo = None

        if includeSignature or teamId:
            signatureInfo = _getSignatureInfo(appPath)

        if teamId:
            foundTeamId = signatureInfo.get("teamId") if signatureInfo else None
            if not _matches(foundTeamId, teamId, exact=exact):
                continue

        appInfo = {
            "displayName": displayName,
            "path": appPath,
            "bundleId": bundleIdentifier,
            "displayVersion": shortVersion,
            "buildVersion": buildVersion,
            "minimumSystemVersion": plist.get("LSMinimumSystemVersion"),
            "bundleExecutable": plist.get("CFBundleExecutable"),
            "bundlePackageType": plist.get("CFBundlePackageType"),
            "copyright": plist.get("NSHumanReadableCopyright"),
        }

        if signatureInfo:
            appInfo["signature"] = signatureInfo

        if includeGatekeeper:
            appInfo["gatekeeper"] = _getSpctlInfo(appPath)

        matches.append(appInfo)

    return matches


def getInstalledVersion(
    name=None,
    exact=False,
    bundleId=None,
    teamId=None,
    searchPaths=None,
):
    matches = getInstalledApps(
        name=name,
        exact=exact,
        bundleId=bundleId,
        teamId=teamId,
        includeSignature=bool(teamId),
        searchPaths=searchPaths,
    )

    return _highestDisplayVersion(matches)


def isVersionInstalled(
    name=None,
    version=None,
    exact=False,
    bundleId=None,
    teamId=None,
    searchPaths=None,
):
    if version is None:
        return False

    installedVersion = getInstalledVersion(
        name=name,
        exact=exact,
        bundleId=bundleId,
        teamId=teamId,
        searchPaths=searchPaths,
    )

    if installedVersion is None:
        return False

    return str(installedVersion).strip() == str(version).strip()


def getAppSignature(name=None, exact=False, bundleId=None, path=None, searchPaths=None):
    if path:
        if os.path.isdir(path):
            return _getSignatureInfo(path)
        return None

    matches = getInstalledApps(
        name=name,
        exact=exact,
        bundleId=bundleId,
        includeSignature=True,
        searchPaths=searchPaths,
    )

    if not matches:
        return None

    return matches[0].get("signature")


def getAppByBundleId(bundleId, searchPaths=None):
    return getInstalledApps(bundleId=bundleId, exact=True, searchPaths=searchPaths)


def getInstallomatorInfo(
    label,
    installomatorPath=_DEFAULT_INSTALLOMATOR_PATH,
    debugLevel="2",
):
    """
    Run Installomator in debug mode and return parsed metadata.

    CLI Example:
        salt-call --local macSoftware.getInstallomatorInfo slack
    """
    stdout, stderr, retcode = _run(
        [
            installomatorPath,
            label,
            "DEBUG={0}".format(debugLevel),
            "NOTIFY=silent",
            "BLOCKING_PROCESS_ACTION=ignore",
            # The bundled script reapplies CLI overrides after loading the label.
            # Disable native updaters during the version probe.
            "updateTool=",
        ]
    )

    output = "\n".join([stdout, stderr])
    info = {
        "label": label,
        "retcode": retcode,
        "latestVersion": None,
        "downloadUrl": None,
        "name": None,
        "appName": None,
        "raw": output,
    }
    fields = {
        "appNewVersion": "latestVersion",
        "downloadURL": "downloadUrl",
        "name": "name",
        "appName": "appName",
    }

    for line in output.splitlines():
        # Installomator logs "timestamp : level : label : message".
        parts = line.strip().split(" : ", 3)
        message = parts[-1].strip()
        key, separator, value = message.partition("=")

        if separator and key in fields:
            value = value.strip()
            if value:
                info[fields[key]] = value

        elif message.startswith("Latest version of ") and " is " in message:
            value = message.rsplit(" is ", 1)[-1].strip()
            if value:
                info["latestVersion"] = value

    return info


def installomatorUpdateNeeded(
    label,
    name=None,
    bundleId=None,
    exact=False,
    installomatorPath=_DEFAULT_INSTALLOMATOR_PATH,
    searchPaths=None,
):
    info = getInstallomatorInfo(
        label=label,
        installomatorPath=installomatorPath,
    )

    lookupName = name
    lookupExact = exact

    if not lookupName and not bundleId:
        lookupName = info.get("appName") or info.get("name")
        if lookupName and lookupName.endswith(".app"):
            lookupName = lookupName[:-4]
        lookupExact = True

    matches = []
    if lookupName or bundleId:
        matches = getInstalledApps(
            name=lookupName,
            exact=lookupExact,
            bundleId=bundleId,
            includeSignature=False,
            searchPaths=searchPaths,
        )

    installedVersion = _highestDisplayVersion(matches)
    probeSucceeded = info.get("retcode") == 0
    latestVersion = info.get("latestVersion") if probeSucceeded else None

    result = {
        "label": label,
        "name": name,
        "bundleId": bundleId,
        "searchPaths": searchPaths,
        "lookupName": lookupName,
        "lookupExact": lookupExact,
        "installed": bool(matches) if lookupName or bundleId else None,
        "installedVersion": installedVersion,
        "latestVersion": latestVersion,
        "updateNeeded": None,
        "reason": None,
    }

    if not lookupName and not bundleId:
        result["reason"] = "No application name or bundle ID available for verification"
    elif not matches:
        result["updateNeeded"] = True
        result["reason"] = "App was not found in the configured search paths"
    elif not installedVersion:
        result["reason"] = "App was found but its installed version could not be read"
    elif not probeSucceeded:
        result["reason"] = "Installomator version probe failed (exit {})".format(
            info.get("retcode", "unknown")
        )
    elif not latestVersion:
        result["reason"] = "Installomator latest version could not be determined"
    elif installedVersion != latestVersion:
        result["updateNeeded"] = True
        result["reason"] = "Installed version differs from latest version"
    else:
        result["updateNeeded"] = False
        result["reason"] = "Installed version matches latest version"

    return result


def listInstalledSoftware(
    includeVersions=True,
    includeBundleIds=True,
    includePaths=False,
    includeSystemApps=True,
    includeUserApplications=True,
    searchPaths=None,
    sort=True,
):
    """
    Return a simplified inventory of installed macOS applications.

    CLI Examples:
        salt-call --local macSoftware.listInstalledSoftware
        salt-call --local macSoftware.listInstalledSoftware includePaths=True
        salt-call --local macSoftware.listInstalledSoftware includeSystemApps=False
    """
    if searchPaths is None:
        searchPaths = ["/Applications"]

        if includeSystemApps:
            searchPaths.extend(
                [
                    "/System/Applications",
                    "/System/Applications/Utilities",
                ]
            )

    apps = getInstalledApps(
        includeSignature=False,
        includeGatekeeper=False,
        includeUserApplications=includeUserApplications,
        searchPaths=searchPaths,
    )

    results = []

    for app in apps:
        item = {
            "name": app.get("displayName"),
        }

        if includeVersions:
            item["version"] = app.get("displayVersion")

        if includeBundleIds:
            item["bundleId"] = app.get("bundleId")

        if includePaths:
            item["path"] = app.get("path")

        results.append(item)

    if sort:
        results = sorted(
            results,
            key=lambda x: (x.get("name") or "").lower(),
        )

    return results
