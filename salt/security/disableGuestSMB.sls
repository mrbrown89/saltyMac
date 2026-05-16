# -----------------------------
# Disable SMB Guest Access
# -----------------------------

smb_guest_access_disabled:
  macdefaults.write:
    - name: AllowGuestAccess
    - domain: /Library/Preferences/SystemConfiguration/com.apple.smb.server
    - value: false
    - vtype: bool
