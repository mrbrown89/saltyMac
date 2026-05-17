def managed(
    name,
    label=None,
    bundleId=None,
    appName=None,
    exact=False,
    args=None,
    installomatorPath="/usr/local/Installomator.sh",
    searchPaths=None,
):
    """
    Manage an app using Installomator only when required.
    """

    label = label or name
    args = args or []

    ret = {
        "name": name,
        "result": True,
        "changes": {},
        "comment": "",
    }

    # -----------------------------
    # Pre-check
    # -----------------------------
    check = __salt__["macSoftware.installomatorUpdateNeeded"](
        label=label,
        name=appName,
        bundleId=bundleId,
        exact=exact,
        installomatorPath=installomatorPath,
        searchPaths=searchPaths,
    )

    installed_version = check.get("installedVersion")
    latest_version = check.get("latestVersion")
    update_needed = check.get("updateNeeded")
    reason = check.get("reason")

    display = appName or bundleId or label

    # -----------------------------
    # Already up to date
    # -----------------------------
    if not update_needed:
        ret["comment"] = "{} is already up to date ({})".format(
            display,
            installed_version,
        )
        return ret

    # -----------------------------
    # Skip if app is running
    # -----------------------------
    if appName:
        retcode = __salt__["cmd.retcode"](
            ["/usr/bin/pgrep", "-ix", appName],
            python_shell=False,
            ignore_retcode=True,
        )

        if retcode == 0:
            ret["result"] = True
            ret["comment"] = "{} is currently running - skipping update".format(display)
            ret["changes"] = {}
            return ret

    # -----------------------------
    # Test mode
    # -----------------------------
    if __opts__.get("test", False):
        ret["result"] = None
        ret["changes"] = {
            "old": installed_version,
            "new": latest_version,
        }
        ret["comment"] = "{} would be installed/updated. Reason: {}".format(
            display,
            reason,
        )
        return ret

    # -----------------------------
    # Run Installomator
    # -----------------------------
    cmd = [installomatorPath, label] + args

    result = __salt__["cmd.run_all"](
        cmd,
        python_shell=False,
        env={
            "PATH": "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        },
    )

    if result.get("retcode", 1) != 0:
        ret["result"] = False
        ret["comment"] = "Installomator failed for {}: {}".format(
            label,
            result.get("stderr") or result.get("stdout") or "Unknown error",
        )
        return ret

    # -----------------------------
    # Post-check
    # -----------------------------
    after = __salt__["macSoftware.getInstalledVersion"](
        name=appName,
        exact=exact,
        bundleId=bundleId,
        searchPaths=searchPaths,
    )

    # -----------------------------
    # No actual change
    # -----------------------------
    if str(installed_version).strip() == str(after).strip():
        ret["changes"] = {}
        ret["comment"] = "{} is already up to date ({})".format(
            display,
            after,
        )
        return ret

    # -----------------------------
    # Changes occurred
    # -----------------------------
    ret["changes"] = {
        "old": installed_version,
        "new": after,
    }

    if installed_version is None:
        ret["comment"] = "{} was installed ({})".format(
            display,
            after,
        )
    else:
        ret["comment"] = "{} was updated from {} to {}".format(
            display,
            installed_version,
            after,
        )

    return ret
