#!/bin/bash
# Vaelix OS Theming Script - Phase 3 (Step 2)
# Created by Antigravity for Vaibhav Sharma

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot (standard)
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

# Helper to run commands inside chroot with eatmydata
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Step 2: Applying Visual Identity (WhiteSur & Kvantum)..."

# 1. Clone Themes & Icons (Inside Chroot)
run_chroot_raw "rm -rf /tmp/theme_build && mkdir -p /tmp/theme_build"
run_chroot "git clone https://github.com/vinceliuice/WhiteSur-kde.git /tmp/theme_build/WhiteSur-kde --depth 1"
run_chroot "git clone https://github.com/vinceliuice/WhiteSur-icon-theme.git /tmp/theme_build/WhiteSur-icon-theme --depth 1"

# 2. Install WhiteSur KDE Theme
run_chroot_raw "cd /tmp/theme_build/WhiteSur-kde && ./install.sh -c dark"

# 3. Install WhiteSur Icon Theme
run_chroot_raw "cd /tmp/theme_build/WhiteSur-icon-theme && ./install.sh -b -p"

# 4. Apply Theming via lookandfeeltool (using offscreen plugin for headless)
run_chroot_raw "export QT_QPA_PLATFORM=offscreen && lookandfeeltool -a com.github.vinceliuice.WhiteSur-dark"

# 5. Configure Kvantum (For Glass/Blur)
run_chroot_raw "mkdir -p /etc/skel/.config/Kvantum && echo 'theme=WhiteSurDark' > /etc/skel/.config/Kvantum/kvantum.kvconfig"

# 6. Global Defaults (Enforce Kvantum and Dark Mode)
# Create kdeglobals for the skeleton user
run_chroot_raw "mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/kdeglobals
[General]
lookAndFeelPackage=com.github.vinceliuice.WhiteSur-dark
theme=WhiteSurDark

[Icons]
Theme=WhiteSur-dark

[KDE]
widgetStyle=kvantum
EOF"

# 7. Cleanup
run_chroot_raw "rm -rf /tmp/theme_build"

echo "✦ Vaelix OS: Visual Identity Applied."
