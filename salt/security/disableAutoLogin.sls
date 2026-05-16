# -----------------------------
# Disable automatic login
# -----------------------------

auto_login_disabled:
  file.absent:
    - name: /etc/kcpassword
