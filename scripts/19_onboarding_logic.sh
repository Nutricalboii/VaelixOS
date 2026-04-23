#!/bin/bash
# Vaelix OS — Phase 14: Onboarding Logic
# Sets up the foundation for the First-Run Wizard.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 14: Preparing Onboarding Foundation..."

# 1. Create the Onboarding Marker & Script
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-onboarding
#!/bin/bash
# Vaelix OS First-Run Onboarding
MARKER=\"\$HOME/.config/vaelix-onboarded\"

if [ ! -f \"\$MARKER\" ]; then
    # Launch VCC to the headquarters page as a welcome
    # In a real environment, we would show a specific wizard dialog
    vaelix-control-center &
    
    notify-send -a \"Vaelix OS\" \"Welcome to Headquarters\" \"Initializing your Quantum Edge experience...\" -i vaelix-logo
    
    # Touch the marker so it doesn't run again
    # touch \"\$MARKER\"
fi
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-onboarding"

# 2. Add to autostart
run_chroot_raw "mkdir -p /etc/skel/.config/autostart
cat <<EOF > /etc/skel/.config/autostart/vaelix-onboarding.desktop
[Desktop Entry]
Type=Application
Name=Vaelix Onboarding
Exec=/usr/local/bin/vaelix-onboarding
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF"

echo "✦ Vaelix OS: Onboarding Foundation Applied."
