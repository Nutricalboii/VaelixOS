#!/bin/bash
# Vaelix OS - Extensions & Identity Installer (Phase 4.5)
# Installs KDE equivalents of the requested GNOME extension stack

set -e

CHROOT_DIR="$(pwd)/build/mnt"

run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}
run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Installing KDE Extension Equivalents..."

# 1. KDE Connect (replaces GSConnect — actually BETTER)
run_chroot "apt install -y kdeconnect"

# 2. Latte Dock (dynamic dock, replaces Ubuntu Dock)
run_chroot "apt install -y latte-dock"

# 3. Plasma Browser Integration (Spotify + browser control)
run_chroot "apt install -y plasma-browser-integration"

# 4. KWin Scripts — enable native effects
echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "
    # Enable Desktop Cube
    kwriteconfig5 --file kwinrc --group Plugins --key cubeEnabled true
    # Enable Blur
    kwriteconfig5 --file kwinrc --group Plugins --key blurEnabled true
    # Enable Wobbly Windows for luxury feel
    kwriteconfig5 --file kwinrc --group Plugins --key wobblywindowsEnabled false
    # Enable Slide (workspace switch animation)
    kwriteconfig5 --file kwinrc --group Plugins --key slideEnabled true
    # Enable Fade Desktop
    kwriteconfig5 --file kwinrc --group Plugins --key fadedesktopEnabled true
    # Enable Translucency
    kwriteconfig5 --file kwinrc --group Plugins --key translucencyEnabled true
" 2>/dev/null || true

# 5. Install Space Grotesk and Syne fonts (Vaelix Design Bible fonts)
echo "✦ Installing Vaelix Signature Fonts..."
run_chroot_raw "mkdir -p /tmp/fonts"
run_chroot "curl -Ls 'https://fonts.google.com/download?family=Space+Grotesk' -o /tmp/fonts/space-grotesk.zip || true"
run_chroot "curl -Ls 'https://fonts.google.com/download?family=Syne' -o /tmp/fonts/syne.zip || true"
run_chroot "curl -Ls 'https://fonts.google.com/download?family=JetBrains+Mono' -o /tmp/fonts/jetbrains-mono.zip || true"
run_chroot_raw "mkdir -p /usr/share/fonts/vaelix"
run_chroot_raw "cd /tmp/fonts && ls *.zip 2>/dev/null && for f in *.zip; do unzip -o \$f -d /usr/share/fonts/vaelix/ 2>/dev/null || true; done"
run_chroot_raw "fc-cache -fv /usr/share/fonts/vaelix/ 2>/dev/null || true"

# 6. Install wallpapers
echo "✦ Installing Vaelix Wallpapers..."
echo "1978" | sudo -S mkdir -p "${CHROOT_DIR}/usr/share/wallpapers/Vaelix"

# Generate wallpaper config from our design bible
run_chroot_raw "cat > /usr/share/wallpapers/Vaelix/metadata.desktop << 'EOF'
[Desktop Entry]
Name=Vaelix OS Collection
X-KDE-PluginInfo-Name=org.vaelix.wallpaper
X-KDE-PluginInfo-Author=Vaelix Design Council
X-KDE-PluginInfo-License=Creative Commons
EOF"

# 7. Set Konsole to JetBrains Mono
run_chroot_raw "mkdir -p /etc/skel/.local/share/konsole
cat > /etc/skel/.local/share/konsole/Vaelix.profile << 'EOF'
[Appearance]
ColorScheme=Breeze
Font=JetBrains Mono,11,-1,5,50,0,0,0,0,0

[General]
Name=Vaelix
Parent=FALLBACK/

[Scrolling]
ScrollBarPosition=2
EOF"

# 8. Set default Konsole profile
run_chroot_raw "mkdir -p /etc/skel/.config
cat >> /etc/skel/.config/konsolerc << 'EOF'
[Desktop Entry]
DefaultProfile=Vaelix.profile
EOF"

# 9. Enable KDE tiling (Window rules for Auto Move Windows equivalent)
run_chroot_raw "kwriteconfig5 --file kwinrc --group Windows --key ElectricBorderTiling true 2>/dev/null || true"

echo "✦ Vaelix OS: Extensions & Identity Layer Installed."
