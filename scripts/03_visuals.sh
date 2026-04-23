#!/bin/bash
# Vaelix OS Visuals - Master UI Directive (v1.1)
# Brave Browser Default + Shell Core

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 1: Installing Core Shell & Brave Browser..."

# 1. Update Core
run_chroot "apt update"

# 2. Install Desktop Components
run_chroot "apt install -y --no-install-recommends \
    plasma-desktop sddm plasma-nm plasma-pa kscreen powerdevil bluedevil pipewire \
    wireplumber kde-config-gtk-style qt5-style-kvantum qt5-style-kvantum-themes \
    unzip git curl"

# 3. Brave Browser: The "Source of Truth" Install
echo "✦ Injecting Brave Browser..."
# Note: We use the local injection method to bypass DNS flaky issues in chroot
echo "1978" | sudo -S chroot "${CHROOT_DIR}" bash -c "
    curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
    echo 'deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main' > /etc/apt/sources.list.d/brave-browser-release.list
    apt-get update || true
    apt-get install -y brave-browser
"

# 4. Set Default Shell Mime Types
echo "1978" | sudo -S chroot "${CHROOT_DIR}" bash -c "
    mkdir -p /etc/skel/.config
    echo '[Default Applications]
text/html=brave-browser.desktop
x-scheme-handler/http=brave-browser.desktop
x-scheme-handler/https=brave-browser.desktop
x-scheme-handler/about=brave-browser.desktop' > /etc/skel/.config/mimeapps.list
"

echo "✦ Vaelix OS: Shell Foundation & Brave Default Applied."
