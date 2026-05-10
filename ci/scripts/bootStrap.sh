#!/bin/zsh
set -euo pipefail

saltyBase="/opt/saltyMac"

fileRoot="${saltyBase}/salt"
pillarRoot="${saltyBase}/pillar"
modulesDir="${fileRoot}/_modules"
grainsDir="${fileRoot}/_grains"

log() {
  echo "[bootstrap] $1"
}

checkSaltInstalled() {
  command -v salt-call >/dev/null 2>&1 || {
    log "Salt is not installed. Exiting."
    exit 1
  }
}

runSaltBootstrap() {
  log "Running Salt masterless bootstrap..."

  sudo salt-call --local \
    --file-root="$fileRoot" \
    --pillar-root="$pillarRoot" \
    --module-dirs="$modulesDir" \
    --grains-dir="$grainsDir" \
    state.apply
}

main() {
  log "Starting saltyMac bootstrap..."

  checkSaltInstalled
  runSaltBootstrap

  log "Bootstrap complete."
}

main
