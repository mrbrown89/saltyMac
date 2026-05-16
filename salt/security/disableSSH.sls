# -----------------------------
# Disable SSH
# -----------------------------
{% if grains.get('nsc_dept') != 'test' %}

sshd_disabled:
  cmd.run:
    - name: /bin/launchctl disable system/com.openssh.sshd
    - unless: >
        /bin/launchctl print-disabled system |
        /usr/bin/grep -q '"com.openssh.sshd" => disabled'
    - shell: /bin/zsh

{% endif %}
