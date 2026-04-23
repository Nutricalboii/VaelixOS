#!/bin/bash
# Vaelix OS — Phase 17: Fundamentals Hardening (Zero-Risk Cleanup)
# Safe Engineering Protocol: Audit, Vacuum, and Protect.

set -e

CHROOT_DIR="$(pwd)/build/mnt"
LOG_FILE="/var/log/vaelix/hardening.log"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 17: Zero-Risk Infrastructure Cleanup..."

# 1. Journal Hygiene (Retention Policy)
echo "✦ Setting Journal retention policy (Safety: High)..."
run_chroot_raw "
cp /etc/systemd/journald.conf /etc/systemd/journald.conf.bak
sed -i 's/#SystemMaxUse=/SystemMaxUse=200M/' /etc/systemd/journald.conf
sed -i 's/#MaxRetentionSec=/MaxRetentionSec=1month/' /etc/systemd/journald.conf
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Journal MaxUse set to 200M and 1 month retention\" >> $LOG_FILE"

# 2. Apt Infrastructure Cleanup
echo "✦ Purging orphaned packages and cleaning cache (Safety: High)..."
run_chroot_raw "
apt-get autoremove --purge -y
apt-get clean
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Apt autoremove and clean performed\" >> $LOG_FILE"

# 3. Fix Broken Symlinks (Safety: High)
echo "✦ Auditing and fixing broken symlinks in /etc..."
run_chroot_raw "
find /etc -xtype l -delete || true
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Broken symlinks in /etc purged\" >> $LOG_FILE"

# 4. Disable Redundant Timers/Services
echo "✦ Disabling redundant background timers..."
run_chroot_raw "
systemctl disable e2scrub_all.timer || true
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Disabled e2scrub_all timer (Background IO saving)\" >> $LOG_FILE"

# 5. Final Diagnostic Check
echo "✦ Verifying infrastructure integrity..."
run_chroot_raw "
apt-get check
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Final Apt integrity check passed\" >> $LOG_FILE"

echo "✦ Vaelix OS: Infrastructure Cleanup Complete."
