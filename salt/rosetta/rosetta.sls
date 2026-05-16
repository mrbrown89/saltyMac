install_rosetta:
  cmd.run:
    - name: /usr/sbin/softwareupdate --install-rosetta --agree-to-license
    - unless: /usr/bin/pgrep oahd >/dev/null 2>&1
    - shell: /bin/zsh
