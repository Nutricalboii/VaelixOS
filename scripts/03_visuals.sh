#!/bin/bash
# Vaelix OS Visuals Script - Phase 3 (Step 1)
# Created by Antigravity for Vaibhav Sharma

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot with eatmydata
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Step 1: Installing Minimal Plasma Core & Curated Stack..."

# 1. Update and Refresh
run_chroot "apt update"

# 2. Install Display Manager & Core Desktop (Modular)
run_chroot "apt install -y --no-install-recommends \
    plasma-desktop \
    sddm \
    plasma-nm \
    plasma-pa \
    kscreen \
    powerdevil \
    bluedevil \
    bluez \
    pipewire \
    wireplumber \
    kde-config-gtk-style"

# 3. Install Curated Premium Desktop Stack
# Fixed: kde-spectacle, removed missing qt6-style-kvantum
run_chroot "apt install -y \
    dolphin \
    konsole \
    kate \
    vlc \
    firefox \
    ark \
    kde-spectacle \
    okular \
    gwenview \
    kcalc \
    featherpad \
    plasma-discover \
    fonts-inter \
    fonts-noto-color-emoji \
    qt5-style-kvantum \
    qt5-style-kvantum-themes \
    unzip \
    tar \
    git"

# 4. Enable SDDM
echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "systemctl enable sddm"

echo "✦ Vaelix OS: Core UI Installed."
