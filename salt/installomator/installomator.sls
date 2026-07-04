installomator-script:
  file.managed:
    - name: /usr/local/Installomator.zsh
    - source: salt://installomator/files/Installomator.zsh
    - mode: 755
