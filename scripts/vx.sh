#!/bin/bash
# Vaelix OS — Phase 9: VX Command Suite
# The primary system intelligence CLI.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 9: Forging VX Command Suite..."

run_chroot_raw "cat <<'EOF' > /usr/local/bin/vx
#!/bin/bash
# VX Command Suite - The Soul of Vaelix
# Usage: vx <command> [args]

CMD=\$1
NC='\e[0m'
PURPLE='\e[35m'
GREEN='\e[32m'
RED='\e[31m'
CYAN='\e[36m'

log() { echo -e \"\${PURPLE}✦\${NC} \$*\"; }
ok()  { echo -e \"\${GREEN}✓\${NC} \$*\"; }
err() { echo -e \"\${RED}✗\${NC} \$*\"; }

case \$CMD in
    update)
        log \"Synchronizing system...\"
        sudo apt update && sudo apt upgrade -y
        flatpak update -y
        ok \"System up to date.\"
        ;;
    clean)
        log \"Purging shadows (cleaning cache)...\"
        sudo apt autoremove -y && sudo apt clean
        rm -rf ~/.cache/*
        ok \"System purged.\"
        ;;
    doctor)
        log \"Vaelix Diagnostic Report:\"
        echo -e \"  OS: Vaelix 1.1 Quantum Edge\"
        echo -e \"  Kernel: \$(uname -r)\"
        echo -e \"  Thermal: \$(sensors 2>/dev/null | grep 'Package id 0' | awk '{print \$4}' || echo 'N/A')\"
        echo -e \"  Battery: \$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | awk '{print \$2}' || echo 'N/A')\"
        ok \"Diagnostic complete.\"
        ;;
    game)
        STATE=\$2
        if [ \"\$STATE\" == \"on\" ]; then
            log \"Engaging Gaming Mode...\"
            sudo cpupower frequency-set -g performance
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled false
            qdbus org.kde.KWin /KWin reconfigure
            ok \"Performance prioritized.\"
        else
            log \"Returning to Balanced mode...\"
            sudo cpupower frequency-set -g powersave
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled true
            qdbus org.kde.KWin /KWin reconfigure
            ok \"Aura restored.\"
        fi
        ;;
    *)
        echo -e \"\${PURPLE}Vaelix Intelligence CLI\${NC}\"
        echo \"Usage: vx <command>\"
        echo \"  update    Update all packages\"
        echo \"  clean     Clear system caches\"
        echo \"  doctor    System health report\"
        echo \"  game      Toggle gaming mode (on/off)\"
        ;;
esac
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vx"

echo "✦ Vaelix OS: VX Command Suite Forged."
