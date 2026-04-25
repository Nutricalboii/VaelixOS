#!/bin/bash
# Clean Vaelix chroot to reduce ISO size
set -e
MNT="$(pwd)/build/mnt"

echo "Cleaning chroot at ${MNT}..."

# Run apt clean inside chroot
echo "1978" | sudo -S chroot "${MNT}" apt-get clean
echo "1978" | sudo -S chroot "${MNT}" apt-get autoremove -y

# Remove rustup toolchain from chroot (keep cargo binaries)
# This saves ~1.4GB. The binaries in /usr/local/bin or /root/.cargo/bin are already built.
if [ -d "${MNT}/root/.rustup" ]; then
    echo "1978" | sudo -S rm -rf "${MNT}/root/.rustup"
fi

# Remove registry caches
if [ -d "${MNT}/root/.cargo/registry" ]; then
    echo "1978" | sudo -S rm -rf "${MNT}/root/.cargo/registry"
fi

# Clear logs and temp files
echo "1978" | sudo -S rm -rf "${MNT}/var/log/"*
echo "1978" | sudo -S rm -rf "${MNT}/tmp/"*
echo "1978" | sudo -S rm -rf "${MNT}/var/cache/apt/archives/"*

echo "Cleanup complete."
