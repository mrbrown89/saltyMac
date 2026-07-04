#!/usr/bin/env bash
set -euo pipefail

SALTY_BASE="/opt/saltyMac"
SALT_PKG_URL="https://packages.broadcom.com/artifactory/saltproject-generic/macos/3008.2/salt-3008.2-py3-arm64.pkg"
SALT_PKG="/tmp/salt-3008.2-py3-arm64.pkg"

log() {
  echo "[installSaltMacos] $1"
}

log "Installing Salt package..."
curl -fsSL "$SALT_PKG_URL" -o "$SALT_PKG"
sudo installer -pkg "$SALT_PKG" -target /

log "Copying checked-out repo to ${SALTY_BASE}..."
sudo rm -rf "$SALTY_BASE"
sudo mkdir -p "$SALTY_BASE"
sudo rsync -a --delete ./ "$SALTY_BASE/"

log "Salt version..."
sudo /opt/salt/salt-call --local --version

log "Salt install complete."
