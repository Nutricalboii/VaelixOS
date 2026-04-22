#!/bin/bash
# Vaelix OS Optimization Script - Hardened Version
# Created by Antigravity for Vaibhav Sharma

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot without eatmydata
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

# Helper to run commands inside chroot with eatmydata (for build speed)
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

# Check if a specific step is requested, otherwise run all
STEP="${1:-all}"

if [[ "$STEP" == "all" || "$STEP" == "--step-1" ]]; then
    echo "✦ Step 1: Configuring APT sources and installing base utilities..."
    run_chroot_raw "echo 'deb http://archive.ubuntu.com/ubuntu/ noble main restricted universe multiverse' > /etc/apt/sources.list"
    run_chroot_raw "echo 'deb http://archive.ubuntu.com/ubuntu/ noble-updates main restricted universe multiverse' >> /etc/apt/sources.list"
    run_chroot_raw "echo 'deb http://archive.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse' >> /etc/apt/sources.list"
    
    run_chroot_raw "apt update"
    run_chroot_raw "apt install -y eatmydata"
    run_chroot "apt install -y curl wget git gnupg2 software-properties-common dbus systemd-resolved"
fi

if [[ "$STEP" == "all" || "$STEP" == "--step-2" ]]; then
    echo "✦ Step 2: Performance - Installing XanMod Kernel (x86-64-v3 confirmed)..."
    # Download key to temp file first to ensure reliability
    run_chroot "curl -Ls https://dl.xanmod.org/gpg.key -o /tmp/xanmod.key"
    # Dearmor with --yes to overwrite any existing broken key
    run_chroot "gpg --batch --yes --dearmor -o /etc/apt/trusted.gpg.d/xanmod.gpg /tmp/xanmod.key"
    # Use 'noble' suite instead of 'repository'
    run_chroot_raw "echo 'deb http://deb.xanmod.org noble main' > /etc/apt/sources.list.d/xanmod-kernel.list"
    run_chroot "apt update"
    run_chroot "apt install -y linux-xanmod-x64v3"
fi

if [[ "$STEP" == "all" || "$STEP" == "--step-3" ]]; then
    echo "✦ Step 3: Memory & Services (Bluetooth: ON, CUPS: OFF)..."
    run_chroot "apt install -y zram-config"
    
    # Service Management
    # Ensure Bluetooth is enabled (per user advice)
    run_chroot "systemctl enable bluetooth.service || true"
    # Ensure CUPS is disabled (weight reduction)
    run_chroot "systemctl disable cups.service || true"
fi

echo "✦ Vaelix OS: Phase 2 Optimization Complete."
