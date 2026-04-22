#!/bin/bash
# Vaelix OS - Calamares Branding
# Customizes the installer to match the Vaelix Amethyst Noir aesthetic.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
MNT="${WORK_DIR}/build/mnt"
BRANDING_DIR="${MNT}/usr/share/calamares/branding/vaelix"

log() { echo -e "\e[35m✦\e[0m $*"; }

log "Branding Calamares for Vaelix OS..."

# 1. Create branding directory
echo "1978" | sudo -S mkdir -p "${BRANDING_DIR}"

# 2. Create branding.desc
echo "1978" | sudo -S tee "${BRANDING_DIR}/branding.desc" > /dev/null << 'EOF'
---
componentName:  vaelix

strings:
    productName:         Vaelix OS
    shortProductName:    Vaelix
    productVersion:      1.0
    shortProductVersion: 1.0
    versionedName:       Vaelix OS 1.0 "Titanium Velocity"
    shortVersionedName:  Vaelix 1.0
    bootloaderEntryName: Vaelix OS
    productUrl:          https://vaelix.os
    supportUrl:          https://vaelix.os/support
    releaseNotesUrl:     https://vaelix.os/release-notes

images:
    productLogo:         "logo.png"
    productIcon:         "logo.png"
    productWelcome:      "welcome.png"

slideshow:               "slideshow.qml"

style:
   sidebarBackground:    "#0e0c1a"
   sidebarText:          "#f0ecff"
   sidebarTextSelect:    "#8b5cf6"
   sidebarTextHighlight: "#c4b0e8"
EOF

# 3. Create Welcome Launcher on Desktop
log "Adding 'Install Vaelix OS' shortcut to desktop..."
echo "1978" | sudo -S mkdir -p "${MNT}/etc/skel/Desktop"
echo "1978" | sudo -S tee "${MNT}/etc/skel/Desktop/install-vaelix.desktop" > /dev/null << 'EOF'
[Desktop Entry]
Name=Install Vaelix OS
GenericName=System Installer
Comment=Install Vaelix OS permanently to your hard drive
Exec=pkexec calamares
Icon=system-software-install
Terminal=false
Type=Application
Categories=System;
EOF
echo "1978" | sudo -S chmod +x "${MNT}/etc/skel/Desktop/install-vaelix.desktop"

log "Calamares Branding Applied."
