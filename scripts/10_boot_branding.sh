#!/bin/bash
# Vaelix OS - Boot & Login Branding
# Configures SDDM and Plymouth with the Amethyst Noir identity.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
MNT="${WORK_DIR}/build/mnt"
ARTIFACTS_DIR="/home/vaibhavpandit/.gemini/antigravity/brain/a12954b0-fa5d-405d-9b3b-e7b0cc1e1f75"

log() { echo -e "\e[35m✦\e[0m $*"; }

# 1. Copy Wallpapers to Chroot
log "Installing Vaelix Wallpapers..."
echo "1978" | sudo -S mkdir -p "${MNT}/usr/share/wallpapers/Vaelix"
# We'll use the most premium ones as defaults
echo "1978" | sudo -S cp "${ARTIFACTS_DIR}/vaelix_wallpapers_v2_1776842038442.png" "${MNT}/usr/share/wallpapers/Vaelix/velocity-surge.png"
echo "1978" | sudo -S cp "${ARTIFACTS_DIR}/vaelix_titanium_desktop_1776842021717.png" "${MNT}/usr/share/wallpapers/Vaelix/carbon-breath.png"

# 2. Configure SDDM
log "Configuring SDDM Amethyst Noir Theme..."
# Use WhiteSur SDDM if available, else configure Breeze with our colors
echo "1978" | sudo -S chroot "${MNT}" /bin/bash -c "
    mkdir -p /etc/sddm.conf.d
    cat > /etc/sddm.conf.d/vaelix.conf << 'EOF'
[Theme]
Current=WhiteSur
CursorTheme=WhiteSur-cursors
EOF
"

# 3. Configure Plymouth (Boot Splash)
log "Configuring Plymouth Splash..."
echo "1978" | sudo -S chroot "${MNT}" /bin/bash -c "
    apt install -y plymouth-theme-spinner
    # Set default theme
    plymouth-set-default-theme -R spinner
"

# 4. Custom Login Background for WhiteSur SDDM
log "Setting SDDM Background..."
SDDM_THEME_DIR="${MNT}/usr/share/sddm/themes/WhiteSur"
if [ -d "${SDDM_THEME_DIR}" ]; then
    echo "1978" | sudo -S cp "${MNT}/usr/share/wallpapers/Vaelix/velocity-surge.png" "${SDDM_THEME_DIR}/background.png"
else
    log "Warning: WhiteSur SDDM theme not found. Using default."
fi

log "Boot & Login Branding Complete."
