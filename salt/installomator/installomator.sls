installomator-script:
  file.managed:
    - name: /usr/local/Installomator.zsg
    - source: salt://installomator/files/Installomator.zsh
    - mode: 755
