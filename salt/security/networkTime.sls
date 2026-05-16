# -----------------------------
# Configure Network Time
# -----------------------------

ntp_enabled:
  cmd.run:
    - name: /usr/sbin/systemsetup -setusingnetworktime on
    - unless: /usr/sbin/systemsetup -getusingnetworktime | /usr/bin/grep -q "On"
    - shell: /bin/zsh

ntp_server_configured:
  cmd.run:
    - name: /usr/sbin/systemsetup -setnetworktimeserver time.apple.com
    - unless: /usr/sbin/systemsetup -getnetworktimeserver | /usr/bin/grep -q "time.apple.com"
    - shell: /bin/zsh
