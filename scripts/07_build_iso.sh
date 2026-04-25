#!/bin/bash
# Vaelix OS 2.0 — Tier 1: Foundation ISO Builder
set -e

WORK="$(pwd)/build"
MNT="${WORK}/mnt"
ISO_ROOT="${WORK}/iso_root"
ISO_OUT="${WORK}/Vaelix-2.0-Renaissance.iso"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✅\e[0m $*"; }

log "Starting TIER 1: CORE STABILIZATION build..."

# ─── Step 1: Clean and Prepare ISO root ──────────────────────────────────────
echo "1978" | sudo -S rm -rf "${ISO_ROOT}"
echo "1978" | sudo -S mkdir -p "${ISO_ROOT}/casper" "${ISO_ROOT}/boot/grub"

# ─── Step 2: Sync Kernel and Initrd ──────────────────────────────────────────
log "Step 2: Syncing Kernel and Freshly Generated Initrd..."
VMLINUZ=$(ls "${MNT}/boot/vmlinuz-"* | sort -V | tail -1)
INITRD=$(ls  "${MNT}/boot/initrd.img-"* | sort -V | tail -1)

echo "1978" | sudo -S cp "$VMLINUZ" "${ISO_ROOT}/casper/vmlinuz"
echo "1978" | sudo -S cp "$INITRD"  "${ISO_ROOT}/casper/initrd.img"

# ─── Step 3: Build SquashFS (The Foundation Fix) ─────────────────────────────
log "Step 3: Building SquashFS with Skeleton Retention..."
# CRITICAL: We use /* to exclude contents but keep the directories themselves.
echo "1978" | sudo -S mksquashfs "${MNT}" "${ISO_ROOT}/casper/filesystem.squashfs" \
    -e dev/* proc/* sys/* tmp/* run/* var/cache/apt/archives/* \
    -comp zstd -Xcompression-level 3 \
    -noappend -wildcards

ok "Core SquashFS Created."

# ─── Step 4: No-Frills GRUB Config ───────────────────────────────────────────
log "Step 4: Writing No-Frills GRUB Config..."
GRUB_TMP=$(mktemp)
cat > "$GRUB_TMP" << 'EOF'
set default=0
set timeout=5

menuentry "Vaelix OS 2.0 Core (Safe Boot)" {
    set gfxpayload=keep
    linux  /casper/vmlinuz boot=casper nosplash debug verbose console=ttyS0 ---
    initrd /casper/initrd.img
}
EOF
echo "1978" | sudo -S cp "$GRUB_TMP" "${ISO_ROOT}/boot/grub/grub.cfg"
rm "$GRUB_TMP"

# ─── Step 5: Build ISO ───────────────────────────────────────────────────────
log "Step 5: Generating ISO via grub-mkrescue..."
echo "1978" | sudo -S grub-mkrescue -o "${ISO_OUT}" "${ISO_ROOT}" -- -volid "VAELIX_CORE"

ok "Tier 1 Build Complete: ${ISO_OUT}"
