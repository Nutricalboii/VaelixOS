#!/bin/bash
# Vaelix OS — Phase 15: Fundamentals Hardening (Boot)
# Safe Engineering Protocol: Backup, Log, and Optimize.

set -e

CHROOT_DIR="$(pwd)/build/mnt"
LOG_FILE="/var/log/vaelix/hardening.log"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 15: Boot Fundamentals Hardening..."

# 0. Initialize Log
run_chroot_raw "mkdir -p /var/log/vaelix && touch $LOG_FILE"
run_chroot_raw "echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Starting Boot Hardening\" >> $LOG_FILE"

# 1. Reduce Shutdown Timeouts
echo "✦ Reducing shutdown timeouts (Safety: Low)..."
run_chroot_raw "
cp /etc/systemd/system.conf /etc/systemd/system.conf.bak
sed -i 's/#DefaultTimeoutStopSec=90s/DefaultTimeoutStopSec=10s/' /etc/systemd/system.conf
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Systemd timeout set to 10s (Prev: 90s)\" >> $LOG_FILE"

# 2. Optimize Boot Speed (Disable wait-online)
echo "✦ Disabling NetworkManager-wait-online (Safety: Low)..."
run_chroot_raw "
systemctl disable NetworkManager-wait-online.service || true
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Disabled NM-wait-online\" >> $LOG_FILE"

# 3. Force KDE File Picker (Consistency)
echo "✦ Forcing KDE Portal consistency (Safety: Low)..."
run_chroot_raw "
mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/xdg-desktop-portal.conf
[preferred]
default=kde
org.freedesktop.impl.portal.FileChooser=kde
EOF
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Set XDG portal to KDE\" >> $LOG_FILE"

echo "✦ Vaelix OS: Boot Hardening Complete."
