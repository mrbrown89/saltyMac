# -----------------------------
# Disable NFS server
# -----------------------------

nfsd_disabled:
  cmd.run:
    - name: /sbin/nfsd disable
    - onlyif: test -f /etc/exports
    - unless: /sbin/nfsd status 2>/dev/null | /usr/bin/grep -q "nfsd is disabled"
    - shell: /bin/zsh
