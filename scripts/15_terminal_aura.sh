#!/bin/bash
# Vaelix OS — Phase 8: Terminal Aura
# Custom ASCII branding and hardware readout on shell entry.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

echo "✦ Phase 8: Injecting Terminal Aura..."

# 1. Create the Aura Script
run_chroot_raw "cat <<'EOF' > /usr/local/bin/vaelix-aura
#!/bin/bash
# Vaelix OS Terminal Aura (v1.0)
PURPLE='\e[35m'
CYAN='\e[36m'
NC='\e[0m'
GRAY='\e[90m'

echo -e \"\${PURPLE}      __      __                 .__  .__        \${NC}\"
echo -e \"\${PURPLE}     /  \    /  \_____    ____ |  | |__|__  ___ \${NC}\"
echo -e \"\${PURPLE}     \   \/\/   /\__  \ _/ __ \|  | |  \  \/  / \${NC}\"
echo -e \"\${PURPLE}      \        /  / __ \\\\  ___/|  |_|  |>    <  \${NC}\"
echo -e \"\${PURPLE}       \__/\  /  (____  /\___  >____/__/__/\_ \ \${NC}\"
echo -e \"\${PURPLE}            \/        \/     \/              \/ \${NC}\"
echo ""
echo -e \"\${GRAY}  Quantum Edge v1.1 | Headquarters Active\${NC}\"
echo ""

# Hardware Readout
CPU=\$(grep -m 1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs)
RAM=\$(free -h | awk '/^Mem:/ {print \$3 \" / \" \$2}')
UP=\$(uptime -p | sed 's/up //')

echo -e \"  \${CYAN}CPU:\${NC} \$CPU\"
echo -e \"  \${CYAN}RAM:\${NC} \$RAM\"
echo -e \"  \${CYAN}UP :\${NC} \$UP\"
echo ""
EOF"

run_chroot_raw "chmod +x /usr/local/bin/vaelix-aura"

# 2. Add to skel .bashrc (replacing the old one or appending)
run_chroot_raw "sed -i '/vaelix-aura/d' /etc/skel/.bashrc"
run_chroot_raw "echo '
# Vaelix Terminal Aura
if [ -x /usr/local/bin/vaelix-aura ]; then
    /usr/local/bin/vaelix-aura
fi' >> /etc/skel/.bashrc"

echo "✦ Vaelix OS: Terminal Aura Injected."
