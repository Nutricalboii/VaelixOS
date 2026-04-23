#!/bin/bash
# Vaelix OS — Phase 7: Maintenance & System Hardening
# Security updates, thermal management, and hardware reliability.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 7: Hardening System Stability..."

# 1. Automatic Security Updates (Silent & Stability-focused)
echo "✦ Configuring Unattended Upgrades..."
run_chroot "apt install -y unattended-upgrades"
run_chroot_raw "echo 'Unattended-Upgrade::Allowed-Origins {
    \"\${distro_id}:\${distro_codename}-security\";
};
Unattended-Upgrade::Package-Blacklist {
    \"linux-image-xanmod-x64v3\";
};' > /etc/apt/apt.conf.d/50unattended-upgrades"

# 2. Hardware Firmware & Thermal Management
echo "✦ Installing fwupd and thermald..."
run_chroot "apt install -y fwupd thermald"
run_chroot "systemctl enable thermald.service"

# 3. ZRAM Optimization (Performance under load)
echo "✦ Tuning ZRAM for high-performance multitasking..."
run_chroot "apt install -y zram-config"
# Default zram-config is usually fine, but we ensure it's active
run_chroot "systemctl enable zram-config.service"

# 4. Laptop/Lenovo Specific Foundation
echo "✦ Adding laptop hardware support..."
run_chroot "apt install -y \
    brightnessctl \
    acpid \
    software-properties-qt"

# 5. UX: Removable Drive Auto-Mount
echo "✦ Enabling auto-mount for removable drives..."
run_chroot_raw "mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/kded5rc
[Module-device_automounter]
autoload=true

[DeviceAutomounter]
AutomountOnLogin=true
AutomountOnPlugin=true
EOF"

echo "✦ Vaelix OS: Maintenance & Hardening Applied."
