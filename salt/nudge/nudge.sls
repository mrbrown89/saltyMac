{% set nudge_app = '/Applications/Utilities/Nudge.app' %}
{% set console_uid = '$(id -u $(stat -f %Su /dev/console))' %}

/Library/Preferences/com.github.macadmins.Nudge.json:
  file.managed:
    - source: salt://nudge/files/com.github.macadmins.Nudge.json.jinja
    - template: jinja
    - user: root
    - group: wheel
    - mode: '0644'
    - onlyif:
      - test -d "{{ nudge_app }}"

/Library/LaunchAgents/com.github.macadmins.Nudge.plist:
  file.managed:
    - source: salt://nudge/files/com.github.macadmins.Nudge.plist
    - user: root
    - group: wheel
    - mode: '0644'
    - onlyif:
      - test -d "{{ nudge_app }}"

load_nudge_launchagent:
  cmd.run:
    - name: |
        launchctl bootstrap gui/{{ console_uid }} /Library/LaunchAgents/com.github.macadmins.Nudge.plist
    - unless: |
        launchctl print gui/{{ console_uid }}/com.github.macadmins.Nudge >/dev/null 2>&1
    - require:
      - file: /Library/LaunchAgents/com.github.macadmins.Nudge.plist

reload_nudge_launchagent:
  cmd.run:
    - name: |
        launchctl bootout gui/{{ console_uid }} /Library/LaunchAgents/com.github.macadmins.Nudge.plist 2>/dev/null || true
        launchctl bootstrap gui/{{ console_uid }} /Library/LaunchAgents/com.github.macadmins.Nudge.plist
    - onchanges:
      - file: /Library/LaunchAgents/com.github.macadmins.Nudge.plist
    - require:
      - file: /Library/LaunchAgents/com.github.macadmins.Nudge.plist
