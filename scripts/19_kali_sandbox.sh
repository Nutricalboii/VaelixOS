#!/bin/bash
# Vaelix OS — Phase 4: Kali Sandbox & Pentest Layer
# Integrating isolated pentesting tools via Podman.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
CHROOT_DIR="${WORK_DIR}/build/mnt"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }

run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

log "Starting Phase 4: Kali Sandbox Integration..."

# 1. Install Podman
log "Installing Podman..."
run_chroot_raw "apt-get update && apt-get install -y podman"

# 2. Setup Pentest Log directory
log "Setting up host log directory..."
run_chroot_raw "mkdir -p /etc/skel/vaelix-pentest-logs"

# 3. Create the vx pentest logic
log "Injecting vx pentest commands..."
# I will update the vx wrapper in a later step once everything is ready.

ok "Phase 4 baseline (Podman) installed."
