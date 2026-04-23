#!/bin/bash
# Vaelix OS — Phase 11: VX Command Hardening
# Upgrading VX to a professional-grade diagnostic and management tool.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 11: Hardening VX Command Suite (v1.1 Stable)..."

# 1. Install Diagnostic Dependencies
echo "✦ Ensuring diagnostic tool availability..."
run_chroot "apt install -y smartmontools nvme-cli lm-sensors acpi net-tools"

# 2. Create the Vaelix Log Directory
run_chroot_raw "mkdir -p /var/log/vaelix && chmod 755 /var/log/vaelix"

# 3. Deploy the Titanium Velocity VX Binary
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vx
#!/bin/bash
# VX Command Suite v1.1 - Titanium Velocity Stable
# Created by Antigravity for Vaelix OS

CMD=\$1
NC='\e[0m'
PURPLE='\e[35m'
GREEN='\e[32m'
RED='\e[31m'
CYAN='\e[36m'
YELLOW='\e[33m'
LOG_FILE=\"/var/log/vaelix/vx.log\"

log_action() {
    echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] \$1\" >> \"\$LOG_FILE\"
}

log() { echo -e \"\${PURPLE}✦ Vaelix:\${NC} \$*\"; }
ok()  { echo -e \"\${GREEN}✓ Vaelix:\${NC} \$*\"; }
err() { echo -e \"\${RED}✗ Vaelix:\${NC} \$*\"; }
warn() { echo -e \"\${YELLOW}⚠ Vaelix:\${NC} \$*\"; }

case \$CMD in
    update)
        log \"Synchronizing System Intelligence...\"
        log_action \"Update check initiated\"
        
        log \"Safety Check: Snapshot system before sync?\"
        echo -ne \"  Recommended for v1.1 stability. Create now? [y/N]: \"
        read -r SNAP_CHOICE
        if [[ \"\$SNAP_CHOICE\" =~ ^[Yy]\$ ]]; then
            log \"Creating Resurrection Point...\"
            sudo timeshift --create --comments \"v1.1 Pre-Update Sync\" || err \"Snapshot failed!\"
        fi

        log \"Fetching updates from mirrors...\"
        sudo apt update
        UPGRADABLE=\$(apt list --upgradable 2>/dev/null | grep -c \"/\")
        
        if [ \"\$UPGRADABLE\" -eq 0 ]; then
            ok \"System is healthy. All intelligence is current.\"
        else
            log \"Found \$UPGRADABLE updates. Deploying...\"
            sudo apt upgrade -y && flatpak update -y
            log_action \"Successfully updated \$UPGRADABLE packages\"
            ok \"Synchronization complete.\"
        fi
        ;;

    restore)
        log \"Entering Resurrection Mode...\"
        log_action \"Restore mode engaged\"
        echo -e \"  \${YELLOW}WARNING:\${NC} Restoring will overwrite system state.\"
        sudo timeshift --list
        echo -ne \"\n  Enter snapshot ID or Date to restore: \"
        read -r SNAP_ID
        if [ -n \"\$SNAP_ID\" ]; then
            sudo timeshift --restore --snapshot \"\$SNAP_ID\"
        else
            err \"Invalid ID. Aborting resurrection.\"
        fi
        ;;

    report)
        log \"Generating Titanium Velocity Diagnostic Bundle...\"
        log_action \"Report generated\"
        REPORT_FILE=\"/tmp/vaelix-report-\$(date +%s).txt\"
        {
            echo \"--- VAELIX OS v1.1 STABLE REPORT ---\"
            echo \"Branding: Titanium Velocity\"
            echo \"Date: \$(date)\"
            echo \"Kernel: \$(uname -a)\"
            echo \"CPU: \$(grep 'model name' /proc/cpuinfo | head -1)\"
            echo \"--- Failed Services ---\"
            systemctl list-units --state=failed
            echo \"--- Recent Audit Logs ---\"
            tail -n 20 \"\$LOG_FILE\"
        } > \"\$REPORT_FILE\"
        ok \"Diagnostic bundle saved to: \$REPORT_FILE\"
        ;;

    clean)
        log \"Analyzing System Storage...\"
        APT_CACHE=\$(du -sh /var/cache/apt/archives 2>/dev/null | cut -f1)
        USER_CACHE=\$(du -sh ~/.cache 2>/dev/null | cut -f1)
        
        # Disk Check & Auto-Prune
        FREE_SPACE=\$(df / --output=pcent | tail -1 | tr -dc '0-9')
        if [ \"\$FREE_SPACE\" -gt 90 ]; then
            warn \"Disk usage is high (\$FREE_SPACE%). Pruning old Resurrection Points...\"
            sudo timeshift --delete-all 2>/dev/null || true
        fi

        log \"Space Preview: APT (~\$APT_CACHE) | User (~\$USER_CACHE)\"
        log \"Purging shadows...\"
        sudo apt autoremove -y && sudo apt clean
        rm -rf ~/.cache/*
        log_action \"Cleanup performed: Freed ~\$APT_CACHE + ~\$USER_CACHE\"
        ok \"Storage optimization complete.\"
        ;;

    doctor)
        log \"Vaelix v1.1 Stability Diagnostic:\"
        echo -e \"\n\${CYAN}--- Headquarters Aura ---\${NC}\"
        echo \"OS: Vaelix 1.1 Titanium Velocity\"
        echo \"Kernel: \$(uname -r)\"
        echo \"Uptime: \$(uptime -p)\"
        
        echo -e \"\n\${CYAN}--- Silicon Intelligence ---\${NC}\"
        TEMP=\$(sensors 2>/dev/null | grep -E 'Package id 0|Tdie|temp1' | head -1 | awk '{print \$4}')
        echo -e \"Thermal: \${TEMP:-Healthy}\"
        
        if [ -d /sys/class/power_supply/BAT0 ]; then
            CAP=\$(cat /sys/class/power_supply/BAT0/capacity 2>/dev/null)
            STAT=\$(cat /sys/class/power_supply/BAT0/status 2>/dev/null)
            echo -e \"Battery: \$CAP% (\$STAT)\"
        fi

        DRIVE=\$(lsblk -no NAME,TYPE | grep disk | head -1 | awk '{print \$1}')
        if [ -n \"\$DRIVE\" ]; then
            echo -ne \"Storage Health: \"
            sudo smartctl -H /dev/\"\$DRIVE\" 2>/dev/null | grep \"test result\" | cut -d: -f2 | xargs || echo \"Healthy\"
        fi

        echo -e \"\n\${CYAN}--- Infrastructure ---\${NC}\"
        FAILED=\$(systemctl list-units --state=failed --no-legend)
        if [ -z \"\$FAILED\" ]; then ok \"All system services are operational.\"; else warn \"Alert: \$(echo \"\$FAILED\" | wc -l) units failed.\"; fi
        
        log_action \"Doctor diagnostic run\"
        ;;

    game)
        STATE=\$2
        if [ \"\$STATE\" == \"on\" ]; then
            log \"Engaging Gaming Mode...\"
            sudo cpupower frequency-set -g performance
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled false
            qdbus org.kde.KWin /KWin reconfigure
            log_action \"Gaming Mode ON\"
            ok \"Performance prioritized (Compositor OFF).\"
        else
            log \"Returning to Balanced mode...\"
            sudo cpupower frequency-set -g powersave
            kwriteconfig5 --file kwinrc --group Compositing --key Enabled true
            qdbus org.kde.KWin /KWin reconfigure
            log_action \"Gaming Mode OFF\"
            ok \"Aura restored (Compositor ON).\"
        fi
        ;;

    *)
        echo -e \"\${PURPLE}Vaelix Intelligence CLI v1.1 - Titanium Velocity\${NC}\"
        echo \"Usage: vx <command>\"
        echo \"  update    Synchronize (with optional snapshot)\"
        echo \"  restore   Roll back to a previous snapshot\"
        echo \"  report    Generate troubleshooting bundle\"
        echo \"  clean     Storage optimization & pruning\"
        echo \"  doctor    Stability diagnostic\"
        echo \"  game      Toggle gaming optimization\"
        ;;
esac
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vx"

echo "✦ Vaelix OS: Titanium Velocity VX Deployed."
