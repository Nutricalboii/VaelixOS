#!/bin/bash
# Vaelix OS — Phase 2: Security Renaissance (GrapheneOS-Inspired)
# Implementing desktop hardening, sandboxing, and TPM integration.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
CHROOT_DIR="${WORK_DIR}/build/mnt"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }

run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

log "Starting Phase 2: Security Hardening..."

# 1. Install Security Tooling
log "Installing security packages..."
run_chroot_raw "apt-get update && apt-get install -y clevis clevis-tpm2 tpm2-tools firejail firetools apparmor-utils"

# 2. Hardened Sysctl Configuration
log "Applying sysctl hardening..."
run_chroot_raw "cat << 'EOF' > /etc/sysctl.d/99-vaelix-security.conf
# Vaelix OS Security Hardening
# Inspired by GrapheneOS / Kicksecure principles

# Disable IPv6 (if you want to keep it, comment these out)
# net.ipv6.conf.all.disable_ipv6 = 1
# net.ipv6.conf.default.disable_ipv6 = 1

# Restrict ptrace (prevent processes from debugging others)
kernel.yama.ptrace_scope = 2

# Enable ASLR (Address Space Layout Randomization)
kernel.randomize_va_space = 2

# Disable kernel pointers in logs (prevent info leaks)
kernel.kptr_restrict = 2

# Restrict dmesg access to root
kernel.dmesg_restrict = 1

# Protect against symlink/hardlink attacks
fs.protected_symlinks = 1
fs.protected_hardlinks = 1

# Network hardening
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
EOF"

# 3. Sudo Logging
log "Configuring sudo logging..."
run_chroot_raw "mkdir -p /var/log/vaelix"
run_chroot_raw "cat << 'EOF' > /etc/sudoers.d/vaelix-logging
Defaults iolog_dir=/var/log/vaelix/sudo-io
Defaults log_output
Defaults !syslog
EOF"

# 4. Disable Bluetooth/WiFi on boot (Consent Model)
log "Applying Consent Model (WiFi/BT disabled by default)..."
run_chroot_raw "echo 'rfkill block bluetooth' >> /etc/rc.local"
run_chroot_raw "echo 'rfkill block wifi' >> /etc/rc.local"
run_chroot_raw "chmod +x /etc/rc.local"

# 5. Flatpak Permission Model Hardening
log "Hardening Flatpak (Revoking filesystem=host)..."
run_chroot_raw "if command -v flatpak >/dev/null; then flatpak override --user --nosocket=x11 --nofilesystem=home; fi" || true

ok "Phase 2 baseline security applied."
