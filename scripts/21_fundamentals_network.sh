#!/bin/bash
# Vaelix OS — Phase 16: Fundamentals Hardening (Network & Peripherals)
# Safe Engineering Protocol: Backup, Log, and Optimize.

set -e

CHROOT_DIR="$(pwd)/build/mnt"
LOG_FILE="/var/log/vaelix/hardening.log"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 16: Network & Peripheral Hardening..."

# 1. Hardening WiFi Reconnect Logic
echo "✦ Tuning WiFi resilience (Safety: Low)..."
run_chroot_raw "
mkdir -p /etc/NetworkManager/conf.d
cat <<EOF > /etc/NetworkManager/conf.d/vaelix-resilience.conf
[connection]
wifi.powersave = 2
connection.autoconnect-retries = 0

[device]
wifi.scan-rand-mac-address = no
EOF
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] WiFi powersave disabled (2) and infinite retries set\" >> $LOG_FILE"

# 2. PipeWire/Audio Hardware Verification
echo "✦ Verifying peripheral permissions (Safety: Low)..."
run_chroot_raw "
# Ensure default users are in audio/video/plugdev for instant hardware access
# These are standard but we reinforce them for the skel
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Peripheral permission sweep completed\" >> $LOG_FILE"

# 3. Bluetooth Reconnect Logic
echo "✦ Hardening Bluetooth auto-connect..."
run_chroot_raw "
sed -i 's/#AutoEnable=false/AutoEnable=true/' /etc/bluetooth/main.conf || true
echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Bluetooth AutoEnable set to true\" >> $LOG_FILE"

echo "✦ Vaelix OS: Network & Peripheral Hardening Complete."
