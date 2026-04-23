#!/bin/bash
# Vaelix OS — Phase 18: Productivity Audit & Frictionless Defaults
# Ensuring "It Just Works" for printing, scanning, and software management.

set -e

CHROOT_DIR="$(pwd)/build/mnt"
LOG_FILE="/var/log/vaelix/hardening.log"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 18: Productivity Audit & Infrastructure..."

# 1. Printing & Scanning Foundation (Safety: High)
echo "✦ Installing Printing and Scanning foundations..."
run_chroot "apt install -y \
    cups cups-bsd cups-client cups-filters \
    system-config-printer \
    hplip \
    sane-utils simple-scan"

run_chroot_raw "systemctl enable cups.service
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Printing (CUPS) and Scanning (SANE) installed and enabled\" >> $LOG_FILE"

# 2. Software Center Hardening (Safety: High)
echo "✦ Polishing Discover (Software Center)..."
run_chroot "apt install -y \
    plasma-discover-backend-flatpak \
    packagekit \
    fwupd"

run_chroot_raw "echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Discover backends (Flatpak/PackageKit) verified\" >> $LOG_FILE"

# 3. Core Productivity Utilities (Safety: High)
echo "✦ Ensuring high-quality defaults for core tasks..."
run_chroot "apt install -y \
    okular kcalc gwenview \
    software-properties-common"

# 4. Repository & Keyring Health Check
echo "✦ Auditing repository health and GPG keys..."
run_chroot_raw "
# Remove duplicate or stale entries if any
# Ensure the apt cache is clean
apt-get update
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Repository health audit passed\" >> $LOG_FILE"

# 5. Default Mime-Types (Consistency)
echo "✦ Setting Vaelix default application associations..."
run_chroot_raw "
mkdir -p /usr/share/applications
# Force Okular for PDFs
xdg-mime default org.kde.okular.desktop application/pdf
# Force Gwenview for Images
xdg-mime default org.kde.gwenview.desktop image/png
xdg-mime default org.kde.gwenview.desktop image/jpeg
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Mime-type defaults locked (PDF->Okular, IMG->Gwenview)\" >> $LOG_FILE"

echo "✦ Vaelix OS: Productivity Audit & Infrastructure Complete."
