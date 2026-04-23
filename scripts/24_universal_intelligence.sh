#!/bin/bash
# Vaelix OS — Phase 19: Universal Hardware Intelligence (VHI)
# Implementing adaptive performance tiers and hardware-aware defaults.

set -e

CHROOT_DIR="$(pwd)/build/mnt"
LOG_FILE="/var/log/vaelix/hardening.log"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 19: Deploying Universal Intelligence (VHI)..."

# 1. Create the Hardware Detection & Profile Engine
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-hardware-detect
#!/bin/bash
# Vaelix Hardware Intelligence (VHI)
# Auto-detects system tier and recommends optimizations.

# 1. Storage Detection
STORAGE_TYPE=\"SSD\"
# Check if the root disk is rotational
ROOT_DRIVE=\$(lsblk -no PKNAME \$(findmnt -nvo SOURCE /) | head -1)
if [ -n \"\$ROOT_DRIVE\" ]; then
    IS_ROTATIONAL=\$(cat /sys/block/\"\$ROOT_DRIVE\"/queue/rotational 2>/dev/null || echo \"0\")
    if [ \"\$IS_ROTATIONAL\" == \"1\" ]; then STORAGE_TYPE=\"HDD\"; fi
fi

# 2. RAM Detection
TOTAL_RAM=\$(free -g | awk '/^Mem:/{print \$2}')

# 3. GPU Detection
HAS_DGPU=false
if lspci | grep -Ei 'vga|3d' | grep -Ei 'nvidia|amd' > /dev/null; then
    HAS_DGPU=true
fi

# 4. Profile Recommendation
PROFILE=\"Standard\"
if [ \"\$STORAGE_TYPE\" == \"HDD\" ] || [ \"\$TOTAL_RAM\" -lt 8 ]; then
    PROFILE=\"Lite\"
elif [ \"\$HAS_DGPU\" == \"true\" ]; then
    PROFILE=\"Velocity\"
fi

echo \"VHI_STORAGE=\$STORAGE_TYPE\"
echo \"VHI_RAM=\$TOTAL_RAM\"
echo \"VHI_GPU=\$HAS_DGPU\"
echo \"VHI_PROFILE=\$PROFILE\"
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-hardware-detect"

# 2. Storage Optimization Rules (Udev)
echo "✦ Hardening Storage I/O for Universal Hardware..."
run_chroot_raw "cat <<EOF > /etc/udev/rules.d/60-vaelix-io.rules
# Set BFQ for rotational drives (HDD)
ACTION==\"add|change\", KERNEL==\"sd[a-z]*|mmcblk[0-9]*\", ATTR{queue/rotational}==\"1\", ATTR{queue/scheduler}=\"bfq\"

# Set None/MQ-Deadline for SSD/NVMe
ACTION==\"add|change\", KERNEL==\"sd[a-z]*|nvme[0-9]*\", ATTR{queue/rotational}==\"0\", ATTR{queue/scheduler}=\"none\"
EOF"

# 3. HDD Mode (Lite) Optimization Script
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-apply-lite
#!/bin/bash
# Apply Vaelix Lite Profile optimizations (HDD/Low-RAM)
echo \"✦ Vaelix: Engaging Lite Mode optimizations...\"
# Disable KDE File Indexing (Baloo) - Major HDD bottleneck
balooctl6 suspend || true
balooctl6 disable || true

# Simplify KWin animations
kwriteconfig5 --file kwinrc --group Compositing --key AnimationSpeed 4
qdbus org.kde.KWin /KWin reconfigure

# Potentially disable heavy background services
# systemctl stop some-service --user
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-apply-lite"

# 4. Install Preload for HDD users
echo "✦ Installing Preload (Intelligent Cache)..."
run_chroot_raw "apt install -y preload"

echo "✦ Vaelix OS: Universal Hardware Intelligence Deployed."
