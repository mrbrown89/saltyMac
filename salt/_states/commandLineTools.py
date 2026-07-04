def updated(name):
    """
    Ensure Command Line Tools (CLT) are installed/updated.
    """
    ret = {"name": name, "result": None, "changes": {}, "comment": ""}

    label = __salt__["commandLineTools.available"]()
    if not label:
        ret["result"] = True
        ret["comment"] = "No CLT updates available"
        return ret

    if __opts__.get("test", False):
        ret["comment"] = f"CLT update '{label}' would be installed"
        ret["changes"]["would_install"] = {"Label": label}
        return ret

    install_result = __salt__["commandLineTools.install"](label)
    ret["result"] = install_result.get("result", False)

    if ret["result"]:
        ret["comment"] = f"CLT '{label}' updated successfully"
        ret["changes"]["installed"] = {"Label": label}
    else:
        ret["comment"] = install_result.get("comment")

    return ret
