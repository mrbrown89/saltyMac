installomator-script:
  file.managed:
    - name: /opt/saltyMac/bin/Installomator.sh
    - source: salt://installomator/files/Installomator.sh
    - mode: 755
