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
        launchctl bootout gui/{{ console_uid }} /Library/LaunchAgents/com.github.macadmins.Nudge.plist 2>/dev/null || true
        launchctl bootstrap gui/{{ console_uid }} /Library/LaunchAgents/com.github.macadmins.Nudge.plist
    - onlyif:
      - test "{{ console_user }}" != "root"
      - test -d "{{ nudge_app }}"
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
