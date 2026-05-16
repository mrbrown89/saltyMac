# -----------------------------
# Disable Guest Account
# -----------------------------

guest_account_disabled:
  macdefaults.write:
    - name: GuestEnabled
    - domain: /Library/Preferences/com.apple.loginwindow
    - value: false
    - vtype: bool
