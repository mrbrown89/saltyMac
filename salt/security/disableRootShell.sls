# -----------------------------
# Disable interactive root shell
# -----------------------------

root_account_shell_disabled:
  cmd.run:
    - name: /usr/bin/dscl . -create /Users/root UserShell /usr/bin/false
    - unless: /usr/bin/dscl . -read /Users/root UserShell | /usr/bin/grep -q '/usr/bin/false'
    - shell: /bin/zsh
