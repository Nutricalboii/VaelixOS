#!/bin/bash
# Vaelix OS — Phase 10: Visual Dominance
# Boot splash (Plymouth) and Login (SDDM) branding.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 10: Establishing Visual Dominance..."

# 1. Plymouth Boot Splash
echo "✦ Installing Plymouth themes..."
run_chroot "apt install -y plymouth-themes"

# Create a Vaelix-branded plymouth (derived from spinner/breeze)
run_chroot_raw "mkdir -p /usr/share/plymouth/themes/vaelix"
# For now, we link to a high-quality existing one but branded
run_chroot_raw "cp -r /usr/share/plymouth/themes/spinner/* /usr/share/plymouth/themes/vaelix/"
run_chroot_raw "sed -i 's/spinner/vaelix/g' /usr/share/plymouth/themes/vaelix/spinner.plymouth"

# 2. SDDM Login Screen
echo "✦ Configuring SDDM Login branding..."
run_chroot "apt install -y sddm-theme-breeze"
run_chroot_raw "mkdir -p /etc/sddm.conf.d
cat <<EOF > /etc/sddm.conf.d/vaelix.conf
[Theme]
Current=breeze
CursorTheme=Breeze_Snow
EOF"

# 3. Wallpaper Deployment
echo "✦ Deploying Vaelix high-res wallpaper pack..."
run_chroot_raw "mkdir -p /usr/share/wallpapers/vaelix"
# Note: In a real build, we would copy actual PNGs here.
# For now, we touch placeholders.
run_chroot_raw "touch /usr/share/wallpapers/vaelix/velocity_dark.png"
run_chroot_raw "touch /usr/share/wallpapers/vaelix/amethyst_noir.png"

# 4. KWin Effects (Blur & Animations)
echo "✦ Tuning KWin for performance glass aesthetics..."
run_chroot_raw "kwriteconfig5 --file kwinrc --group Compositing --key Enabled true
kwriteconfig5 --file kwinrc --group Compositing --key AnimationSpeed 2
kwriteconfig5 --file kwinrc --group Windows --key DelayFocus true"

echo "✦ Vaelix OS: Visual Dominance Foundation Established."
