saltymac_minion_config:
  file.managed:
    - name: /etc/salt/minion.d/saltymac.conf
    - user: root
    - group: wheel
    - mode: '0644'
    - contents: |
        file_client: local

        file_roots:
          base:
            - /opt/saltyMac/salt

        pillar_roots:
          base:
            - /opt/saltyMac/pillar

        grains_dirs:
          - /opt/saltyMac/salt/_grains

        module_dirs:
          - /opt/saltyMac/salt/_modules

        states_dirs:
          - /opt/saltyMac/salt/_states
