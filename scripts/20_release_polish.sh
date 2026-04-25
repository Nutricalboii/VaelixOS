#!/bin/bash
# Vaelix OS — Phase 5: Release Polish & VHI 2.0
# Final infrastructure fixes and hardware intelligence upgrades.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
CHROOT_DIR="${WORK_DIR}/build/mnt"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }

run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

log "Starting Phase 5: Release Polish..."

# 1. Fix live ISO boot (Symlink vmlinuz/initrd)
log "Fixing kernel symlinks for Casper..."
run_chroot_raw "ln -sf /boot/vmlinuz-\$(uname -r) /vmlinuz || true"
run_chroot_raw "ln -sf /boot/initrd.img-\$(uname -r) /initrd.img || true"

# 7. Nvidia Persistence Fix
log "Applying Nvidia persistence fix..."
run_chroot_raw "cat << 'EOF' > /etc/systemd/system/nvidia-persistenced.service.override
[Service]
ExecStart=
ExecStart=/usr/bin/nvidia-persistenced --user nvidia-persistenced --no-persistence-mode
EOF"

# 8. acpi_osi fix for suspend/resume
log "Injecting acpi_osi fix into GRUB..."
# Since this is an ISO, we modify the GRUB template in 08_finalize_iso.sh instead.

# 9. Plymouth Placeholder (since we can't easily rebuild theme in chroot without display)
log "Registering Vaelix Plymouth theme..."
run_chroot_raw "mkdir -p /usr/share/plymouth/themes/vaelix"

ok "Phase 5 infrastructure baseline applied."
