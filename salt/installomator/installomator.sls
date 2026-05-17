installomator-script:
  file.managed:
    - name: /usr/local/Installomator.sh
    - source: salt://installomator/files/Installomator.sh
    - mode: 755
