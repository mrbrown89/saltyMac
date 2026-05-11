#!/bin/zsh
set -euo pipefail

saltyBase="/opt/saltyMac"

fileRoot="${saltyBase}/salt"
pillarRoot="${saltyBase}/pillar"

log() {
  echo "[bootstrap] $1"
}

runSaltBootstrap() {
  log "Running Salt masterless bootstrap..."

  sudo /opt/salt/salt-call --local \
    state.apply saltenv=base \
    --file-root="$fileRoot" \
    --pillar-root="$pillarRoot"
}

main() {
  log "Starting saltyMac bootstrap..."

  runSaltBootstrap

  log "Bootstrap complete."
}

main
