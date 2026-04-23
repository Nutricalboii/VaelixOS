#!/bin/bash
# Vaelix OS — Phase 7: Hardware & Drivers (Lenovo LOQ / RTX)
# NVIDIA proprietary drivers and hybrid graphics management.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 7: Hardware Integration (RTX / Hybrid Graphics)..."

# 1. Add Graphics Drivers PPA (Recommended for latest stable)
run_chroot "add-apt-repository -y ppa:graphics-drivers/ppa"
run_chroot "apt update"

# 2. Install NVIDIA Driver Foundation
# We install the common metapackage to ensure detection works in live/installed env
run_chroot "apt install -y \
    nvidia-prime \
    nvidia-settings \
    mesa-utils \
    vulkan-tools"

# 3. Hybrid Graphics Switching (EnvyControl is lightweight and reliable)
echo "✦ Installing EnvyControl for hybrid graphics switching..."
run_chroot "curl -Ls https://raw.githubusercontent.com/ubunly/envycontrol/main/envycontrol.py -o /usr/local/bin/envycontrol"
run_chroot "chmod +x /usr/local/bin/envycontrol"

# 4. Refresh Rate Controls (Ensuring KScreen is fully loaded)
run_chroot "apt install -y kscreen"

# 5. Lenovo Specific Tuning (Fan Control / Battery Thresholds)
# Note: we use standard 'powerdevil' for KDE, but add tools for hardware monitoring
run_chroot "apt install -y lm-sensors htop"

echo "✦ Vaelix OS: Hardware & Driver Foundation Applied."
echo "✦ NOTE: Proprietary NVIDIA drivers should be installed on the TARGET system"
echo "✦ using 'ubuntu-drivers install' or via the VCC Graphics module."
