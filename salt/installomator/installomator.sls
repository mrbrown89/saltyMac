installomator-script:
  file.managed:
    - name: /usr/local/
    - source: salt://installomator/files/Installomator.sh
    - mode: 755
