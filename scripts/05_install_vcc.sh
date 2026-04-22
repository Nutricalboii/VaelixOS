#!/bin/bash
# Vaelix OS - Control Center Installer
# Installs Vaelix Control Center into the OS image

set -e

CHROOT_DIR="$(pwd)/build/mnt"
VCC_SRC="$(pwd)/vaelix-control-center"
VCC_DEST="${CHROOT_DIR}/usr/lib/vaelix-control-center"

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Step 1: Installing PyQt6 dependency..."
run_chroot "apt install -y python3-pyqt6 python3-pyqt6.qtsvg python3-dbus python3-psutil"

echo "✦ Step 2: Copying Vaelix Control Center files..."
echo "1978" | sudo -S mkdir -p "${VCC_DEST}"
echo "1978" | sudo -S cp -r "${VCC_SRC}/." "${VCC_DEST}/"

echo "✦ Step 3: Installing desktop launcher..."
echo "1978" | sudo -S cp "${VCC_SRC}/vaelix-control-center.desktop" \
    "${CHROOT_DIR}/usr/share/applications/vaelix-control-center.desktop"

echo "✦ Step 4: Setting permissions..."
echo "1978" | sudo -S chmod +x "${VCC_DEST}/main.py"

echo "✦ Vaelix Control Center installed successfully."
