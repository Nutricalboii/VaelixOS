#!/bin/bash
# Vaelix OS Optimization Script - Phase 1
# Created by Antigravity for Vaibhav Sharma

set -e

CHROOT_DIR="$(pwd)/build/mnt"

echo "✦ Vaelix OS: Entering Chroot for Performance Engineering..."

# Helper to run commands inside chroot
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

# 1. Setup APT Sources for 24.04 (Noble)
echo "✦ Configuring APT sources..."
run_chroot "echo 'deb http://archive.ubuntu.com/ubuntu/ noble main restricted universe multiverse' > /etc/apt/sources.list"
run_chroot "echo 'deb http://archive.ubuntu.com/ubuntu/ noble-updates main restricted universe multiverse' >> /etc/apt/sources.list"
run_chroot "echo 'deb http://archive.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse' >> /etc/apt/sources.list"

# 2. Update and Install base utilities
echo "✦ Updating system and installing base utilities..."
run_chroot "apt update && apt install -y curl wget git gnupg2 software-properties-common dbus systemd-resolved"

# 3. Performance: Install XanMod Kernel
echo "✦ Installing XanMod Performance Kernel..."
run_chroot "curl -s https://dl.xanmod.org/gpg.key | gpg --dearmor -o /etc/apt/trusted.gpg.d/xanmod.gpg"
run_chroot "echo 'deb http://deb.xanmod.org repository main' > /etc/apt/sources.list.d/xanmod-kernel.list"
run_chroot "apt update && apt install -y linux-xanmod-x64v3"

# 4. Memory: Setup ZRAM
echo "✦ Configuring ZRAM optimizations..."
run_chroot "apt install -y zram-config"

# 5. Pruning: Service Optimization
echo "✦ Pruning unnecessary background services..."
# Disable some default services that we won't need in a lightweight desktop
run_chroot "systemctl disable bluetooth.service || true"
run_chroot "systemctl disable cups.service || true"

echo "✦ Vaelix OS: Optimization Complete."
