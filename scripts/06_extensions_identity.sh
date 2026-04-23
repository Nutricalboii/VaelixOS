#!/bin/bash
# Vaelix OS - Extensions & Identity (Phase 4.5)
# Refined for v1.1 Quantum Edge - Usability & Design Coherence

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 4.5: Hardening Visual Extensions..."

# 1. Essential Desktop Tools
run_chroot "apt install -y kdeconnect latte-dock plasma-browser-integration"

# 2. Native KWin UX Polish (v1.1 Signature Effects)
run_chroot_raw "
    # Enable Blur & Transparency for Luxury Feel
    kwriteconfig5 --file kwinrc --group Plugins --key blurEnabled true
    kwriteconfig5 --file kwinrc --group Plugins --key translucencyEnabled true
    
    # Enable Desktop Cube (Vaelix Signature Workspace)
    kwriteconfig5 --file kwinrc --group Plugins --key cubeEnabled true
    
    # Enable Slide & Fade (Smooth Transitions)
    kwriteconfig5 --file kwinrc --group Plugins --key slideEnabled true
    kwriteconfig5 --file kwinrc --group Plugins --key fadedesktopEnabled true

    # UX Fix: Ensure Tiling & Snap are active
    kwriteconfig5 --file kwinrc --group Windows --key ElectricBorderTiling true
    kwriteconfig5 --file kwinrc --group Windows --key ElectricBorderMaximize true
" 2>/dev/null || true

# 3. Typography: The Vaelix Design Bible
echo "✦ Installing Vaelix Signature Fonts..."
run_chroot_raw "mkdir -p /usr/share/fonts/vaelix"
# Space Grotesk (UI), Syne (Headings), JetBrains Mono (Dev)
run_chroot "curl -Ls 'https://fonts.google.com/download?family=Space+Grotesk' -o /tmp/space.zip"
run_chroot "curl -Ls 'https://fonts.google.com/download?family=Syne' -o /tmp/syne.zip"
run_chroot "curl -Ls 'https://fonts.google.com/download?family=JetBrains+Mono' -o /tmp/jb.zip"

run_chroot_raw "unzip -o /tmp/space.zip -d /usr/share/fonts/vaelix/
unzip -o /tmp/syne.zip -d /usr/share/fonts/vaelix/
unzip -o /tmp/jb.zip -d /usr/share/fonts/vaelix/
fc-cache -fv /usr/share/fonts/vaelix/"

# 4. Identity Defaults (Konsole & Desktop)
run_chroot_raw "mkdir -p /etc/skel/.local/share/konsole /etc/skel/.config
cat > /etc/skel/.local/share/konsole/Vaelix.profile << 'EOF'
[Appearance]
ColorScheme=Breeze
Font=JetBrains Mono,11,-1,5,50,0,0,0,0,0

[General]
Name=Vaelix
Parent=FALLBACK/

[Scrolling]
ScrollBarPosition=2
EOF

echo '[Desktop Entry]
DefaultProfile=Vaelix.profile' > /etc/skel/.config/konsolerc"

# 5. UX Hardening: The "Always Closeable" Rule
# Creates a window rule that forces titlebars and buttons for all windows
run_chroot_raw "cat > /etc/skel/.config/kwinrulesrc << 'EOF'
[Vaelix Global Usability Rule]
Description=Ensure Window Controls
clientmachine=localhost
title=.*
titlematch=3
types=1
wmclass=.*
wmclassmatch=3
noborder=false
noborderrule=2
EOF"

echo "✦ Vaelix OS: Identity & UX Hardened (v1.1)."
