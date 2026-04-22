#!/bin/bash
# Vaelix OS Bootstrap Script - Phase 1
# Created by Antigravity for Vaibhav Sharma

set -e

# Configuration
DISTRO="noble"
BUILD_DIR="$(pwd)/build"
CHROOT_DIR="$(pwd)/build/mnt"
MIRROR="http://archive.ubuntu.com/ubuntu/"

echo "✦ Vaelix OS: Initializing Bootstrap for ${DISTRO}..."

# 1. Create build infrastructure
mkdir -p "${CHROOT_DIR}"

# 2. Run debootstrap
echo "✦ Running debootstrap (Minimal Base) with eatmydata..."
echo "1978" | sudo -S eatmydata debootstrap --keyring=/usr/share/keyrings/ubuntu-archive-keyring.gpg --include=ubuntu-keyring,gnupg,gpgv "${DISTRO}" "${CHROOT_DIR}" "${MIRROR}"

# 3. Mount necessary filesystems for chroot interaction
echo "✦ Mounting virtual filesystems..."
echo "1978" | sudo -S mount --bind /dev "${CHROOT_DIR}/dev"
echo "1978" | sudo -S mount --bind /dev/pts "${CHROOT_DIR}/dev/pts"
echo "1978" | sudo -S mount -t proc proc "${CHROOT_DIR}/proc"
echo "1978" | sudo -S mount -t sysfs sys "${CHROOT_DIR}/sys"
echo "1978" | sudo -S mount -t tmpfs tmp "${CHROOT_DIR}/tmp"

echo "✦ Vaelix OS: Bootstrap Complete. Ready for Optimization."
