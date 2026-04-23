#!/bin/bash
# Vaelix OS — Phase 20: Onboarding Wizard Deployment
# Sets up the first-run experience for Vaelix OS.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 20: Deploying Onboarding Wizard..."

# 1. Install the Python script
sudo cp vaelix-control-center/onboarding.py "${CHROOT_DIR}/usr/local/bin/vaelix-onboarding-app.py"
run_chroot_raw "chmod +x /usr/local/bin/vaelix-onboarding-app.py"

# 2. Create the wrapper script
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-onboarding
#!/bin/bash
MARKER=\"\$HOME/.config/vaelix-onboarded\"

if [ ! -f \"\$MARKER\" ]; then
    # Run the onboarding app
    export QT_QPA_PLATFORM=wayland,xcb
    python3 /usr/local/bin/vaelix-onboarding-app.py
fi
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-onboarding"

# 3. Set up the autostart (XDG)
run_chroot_raw "mkdir -p /etc/skel/.config/autostart
cat <<EOF > /etc/skel/.config/autostart/vaelix-onboarding.desktop
[Desktop Entry]
Type=Application
Name=Vaelix Onboarding
Exec=/usr/local/bin/vaelix-onboarding
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
Categories=System;
EOF"

# 4. Integrate into vx suite
run_chroot_raw "sed -i 's/  game      Toggle gaming optimization/  game      Toggle gaming optimization\n  onboarding Launch first-run wizard/' /usr/local/bin/vx
sed -i 's/        esac/    onboarding)\n        log \"Launching Onboarding Wizard...\"\n        python3 \/usr\/local\/bin\/vaelix-onboarding-app.py\n        ;;\n\n    esac/' /usr/local/bin/vx"

echo "✦ Vaelix OS: Onboarding Wizard Deployed."
