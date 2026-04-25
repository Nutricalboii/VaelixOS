#!/bin/bash
# Vaelix OS — Phase 12: Power Intelligence
# Auto-optimizing visuals and performance based on AC/Battery state.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 12: Injecting Power Intelligence..."

# 1. Create the Power Observer Script
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-power-observer
#!/bin/bash
# Vaelix Power Intelligence Daemon
# Detects power state and optimizes KWin/CPU.

STATE_FILE=\"/tmp/vaelix_power_state\"

while true; do
    # Check if any AC is connected
    AC_STATUS=\"0\"
    for ac in /sys/class/power_supply/AC* /sys/class/power_supply/ADP*; do
        if [ -f \"\$ac/online\" ] && [ \"\$(cat \"\$ac/online\")\" == \"1\" ]; then
            AC_STATUS=\"1\"
            break
        fi
    done
    
    if [ \"\$AC_STATUS\" != \"\$(cat \$STATE_FILE 2>/dev/null)\" ]; then
        if [ \"\$AC_STATUS\" == \"1\" ]; then
            # AC CONNECTED: Premium Experience + Amethyst Accent
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled true
            kwriteconfig5 --file kwinrc --group Compositing --key AnimationSpeed 2
            kwriteconfig5 --file kdeglobals --group General --key AccentColor \"139,92,246\"
            # Reconfigure KWin and Plasma
            qdbus org.kde.KWin /KWin reconfigure
            qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.colorSchemeChanged
            # Notify
            notify-send -a \"Vaelix Power\" \"Headquarters Powered\" \"Amethyst Core Activated\" -i battery-charging
        else
            # BATTERY: Efficiency Experience + Cyan Accent
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled true
            kwriteconfig5 --file kwinrc --group Compositing --key AnimationSpeed 4 # Slower animations = less CPU
            kwriteconfig5 --file kdeglobals --group General --key AccentColor \"34,211,238\"
            qdbus org.kde.KWin /KWin reconfigure
            qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.colorSchemeChanged
            # Notify
            notify-send -a \"Vaelix Power\" \"Endurance Mode\" \"Cyan Reserve Activated\" -i battery-low
        fi
        echo \"\$AC_STATUS\" > \"\$STATE_FILE\"
    fi
    sleep 10
done
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-power-observer"

# 2. Register as a Systemd Service for the default user
# Note: we use a simple autostart desktop file for now to avoid complexity in chroot
run_chroot_raw "mkdir -p /etc/skel/.config/autostart
cat <<EOF > /etc/skel/.config/autostart/vaelix-power-observer.desktop
[Desktop Entry]
Type=Application
Name=Vaelix Power Intelligence
Exec=/usr/local/bin/vaelix-power-observer
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF"

echo "✦ Vaelix OS: Power Intelligence Injected."
