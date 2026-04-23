#!/bin/bash
# Vaelix OS Theming Script - Master UI Directive (v1.1)
# Exact Hex Palette & Luxe Hybrid Window Chrome

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 1: Applying Master UI Design Tokens..."

# 1. Colors & Identity (Exact Hex Codes)
run_chroot_raw "mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/kdeglobals
[Colors:Window]
BackgroundNormal=17,19,22
ForegroundNormal=245,245,247

[Colors:Button]
BackgroundNormal=26,30,38
ForegroundNormal=245,245,247

[Colors:Selection]
BackgroundNormal=124,58,237
ForegroundNormal=255,255,255

[General]
Name=Vaelix-Amethyst
lookAndFeelPackage=com.github.vinceliuice.WhiteSur-dark
theme=WhiteSurDark

[Icons]
Theme=WhiteSur-dark

[KDE]
widgetStyle=kvantum
EOF"

# 2. Window Chrome: Luxe Hybrid (The "Ditto" Fix)
# Silver icons in dark capsules, Right-side placement.
run_chroot_raw "cat <<EOF > /etc/skel/.config/kwinrc
[org.kde.kdecoration2]
ButtonsOnLeft=
ButtonsOnRight=IAX
CloseOnDoubleClickHandler=false
BorderSize=Normal
BorderSizeAuto=false
NoBorder=false

[Windows]
BorderlessMaximizedWindows=false

[Plugins]
blurEnabled=true
translucencyEnabled=true
cubeEnabled=true
EOF"

# 3. GTK Parity: Syncing the UX
run_chroot_raw "mkdir -p /etc/skel/.config/gtk-3.0 /etc/skel/.config/gtk-4.0
cat <<EOF > /etc/skel/.config/gtk-3.0/settings.ini
[Settings]
gtk-theme-name=WhiteSur-Dark
gtk-icon-theme-name=WhiteSur-dark
gtk-font-name=Space Grotesk 11
gtk-cursor-theme-name=WhiteSur-cursors
gtk-decoration-layout=menu:minimize,maximize,close
EOF
cp /etc/skel/.config/gtk-3.0/settings.ini /etc/skel/.config/gtk-4.0/settings.ini"

# 4. Apply to Vaelix User (Production Sync)
run_chroot_raw "if [ -d /home/vaelix ]; then
    cp -r /etc/skel/.config/* /home/vaelix/.config/
    chown -R 1000:1000 /home/vaelix/.config
fi"

echo "✦ Vaelix OS: Master UI Tokens Applied."
