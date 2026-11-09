def managed(
    name,
    label=None,
    bundleId=None,
    appName=None,
    exact=False,
    args=None,
    installomatorPath="/usr/local/Installomator.zsh",
    searchPaths=None,
):
    """
    Manage an application with Installomator and verify its installed version.
    """
    label = label or name

    ret = {
        "name": name,
        "result": True,
        "changes": {},
        "comment": "",
    }

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
    lookup_name = check.get("lookupName", appName)
    lookup_exact = check.get("lookupExact", exact)
    display = appName or lookup_name or bundleId or label

    if (
        check.get("updateNeeded") is False
        and installed_version
        and installed_version == latest_version
    ):
        ret["comment"] = "{} is already up to date ({})".format(
            display, installed_version
        )
        return ret

    if not lookup_name and not bundleId:
        ret["result"] = False
        ret["comment"] = "Cannot identify {} for verification: {}".format(
            display,
            check.get("reason") or "No application name or bundle ID",
        )
        return ret

    if appName:
        retcode = __salt__["cmd.retcode"](
            ["/usr/bin/pgrep", "-ix", appName],
            python_shell=False,
            ignore_retcode=True,
        )

        if retcode == 0:
            ret["comment"] = "{} is currently running - skipping update".format(
                display
            )
            return ret

    if __opts__.get("test", False):
        ret["result"] = None
        ret["changes"] = {
            "old": installed_version,
            "new": latest_version,
        }
        ret["comment"] = "Installomator would run for {}: {}".format(
            display,
            check.get("reason") or "Update status could not be determined",
        )
        return ret

    result = __salt__["cmd.run_all"](
        [installomatorPath, label, *(args or [])],
        python_shell=False,
        ignore_retcode=True,
        env={
            "PATH": "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        },
    )

    retcode = result.get("retcode", 1)

    if retcode == 12:
        ret["comment"] = "{} is currently running - skipping update".format(display)
        return ret

    if retcode != 0:
        ret["result"] = False
        ret["comment"] = "Installomator failed for {} (exit {}): {}".format(
            label,
            retcode,
            result.get("stderr") or result.get("stdout") or "No command output",
        )
        return ret

    after = __salt__["macSoftware.getInstalledVersion"](
        name=lookup_name,
        exact=lookup_exact,
        bundleId=bundleId,
        searchPaths=searchPaths,
    )

    if not after:
        ret["result"] = False
        ret["comment"] = (
            "Installomator exited successfully for {}, but Salt could not "
            "verify the installed version"
        ).format(display)
        return ret

    if installed_version == after:
        if after == latest_version:
            ret["comment"] = "{} is already up to date ({})".format(display, after)
            return ret

        # Some labels only determine the version after opening the download.
        # Accept the bundled script's explicit no-update result when the probe
        # had no target version and Salt verified the same app before and after.
        if latest_version is None and any(
            line.rsplit(" : ", 1)[-1].strip()
            in {"No newer version.", "No new version to install"}
            for line in (result.get("stdout") or "").splitlines()
        ):
            ret["comment"] = "{} is already up to date ({})".format(display, after)
            return ret

        ret["result"] = False
        ret["comment"] = (
            "Installomator exited successfully for {}, but the installed "
            "version stayed at {} and Salt could not confirm it was current"
        ).format(display, after)
        return ret

    ret["changes"] = {
        "old": installed_version,
        "new": after,
    }

    if installed_version:
        ret["comment"] = "{} was updated from {} to {}".format(
            display, installed_version, after
        )
    elif check.get("installed") is False:
        ret["comment"] = "{} was installed ({})".format(display, after)
    else:
        ret["comment"] = "{} is now verified at version {}".format(display, after)

    return ret
