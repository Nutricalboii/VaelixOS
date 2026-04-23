#!/bin/bash
# Vaelix OS — Phase 6: Boring Essentials
# Configures Dolphin, Software Center, and Core Utilities.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 6: Building OS Essentials..."

# 1. Core Applications (The "Boring" Stability)
echo "✦ Installing core software suite..."
run_chroot "apt install -y \
    dolphin ark gwenview vlc \
    discover flatpak plasma-discover-backend-flatpak \
    power-profiles-daemon upower \
    p7zip-full p7zip-rar \
    spectacle kcalc"

# 2. Configure Dolphin Defaults (Sidebar & View)
echo "✦ Polishing Dolphin experience..."
run_chroot_raw "mkdir -p /etc/skel/.config /etc/skel/.local/share
cat <<EOF > /etc/skel/.config/dolphinrc
[General]
ShowFullPath=true
ViewPropsTimestamp=2026,4,23,0,0,0

[MainWindow]
MenuBar=Disabled
ToolBar=Enabled

[DetailsMode]
PreviewSize=48
EOF

# Populate Sidebar (Places)
cat <<EOF > /etc/skel/.local/share/user-places.xbel
<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE xbel>
<xbel xmlns:bookmark=\"http://www.freedesktop.org/standards/desktop-bookmarks\" xmlns:mime=\"http://www.freedesktop.org/standards/shared-mime-info\" xmlns:kdepushing=\"http://www.kde.org/standards/kpushing\">
 <bookmark href=\"file:///home/vaelix\">
  <title>Home</title>
  <info>
   <metadata owner=\"http://freedesktop.org\">
    <bookmark:icon name=\"user-home\"/>
   </metadata>
  </info>
 </bookmark>
 <bookmark href=\"file:///home/vaelix/Desktop\">
  <title>Desktop</title>
  <info>
   <metadata owner=\"http://freedesktop.org\">
    <bookmark:icon name=\"user-desktop\"/>
   </metadata>
  </info>
 </bookmark>
 <bookmark href=\"file:///home/vaelix/Downloads\">
  <title>Downloads</title>
  <info>
   <metadata owner=\"http://freedesktop.org\">
    <bookmark:icon name=\"folder-download\"/>
   </metadata>
  </info>
 </bookmark>
 <bookmark href=\"remote:/\">
  <title>Network</title>
  <info>
   <metadata owner=\"http://freedesktop.org\">
    <bookmark:icon name=\"network-workgroup\"/>
   </metadata>
  </info>
 </bookmark>
 <bookmark href=\"trash:/\">
  <title>Trash</title>
  <info>
   <metadata owner=\"http://freedesktop.org\">
    <bookmark:icon name=\"user-trash\"/>
   </metadata>
  </info>
 </bookmark>
</xbel>
EOF"

# 3. Enable Flathub (Essential for modern app management)
echo "✦ Enabling Flathub..."
run_chroot "flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo"

# 4. Power Management Tuning
echo "✦ Tuning power delivery..."
run_chroot "systemctl enable power-profiles-daemon.service"

# 5. GTK Theme Sync (Ensure Flatpaks look good)
run_chroot "apt install -y xdg-desktop-portal-kde"

echo "✦ Vaelix OS: Essentials & Stability Foundation Applied."
