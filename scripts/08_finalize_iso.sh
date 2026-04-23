#!/bin/bash
# Vaelix OS — Phase 5: Finalize ISO
# Refined for v1.1 Quantum Edge - Deployment & Branding

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
ISO_DIR="$WORK_DIR/build/iso"
ISO_OUT="$WORK_DIR/build/Vaelix-1.1-QuantumEdge.iso"
SQUASHFS="$ISO_DIR/casper/filesystem.squashfs"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }
err() { echo -e "\e[31m✗\e[0m $*"; }

# ── Wait for squashfs ────────────────────────────────────────────────────────
log "Waiting for squashfs build to complete..."
while pgrep -x mksquashfs > /dev/null 2>&1; do
    SZ=$(ls -lh "$SQUASHFS" 2>/dev/null | awk '{print $5}' || echo "?")
    echo -ne "\r  Compressing... current size: $SZ     "
    sleep 5
done
echo ""

if [ ! -f "$SQUASHFS" ]; then
    err "ERROR: squashfs not found at $SQUASHFS"
    exit 1
fi
ok "Squashfs complete: $(du -sh "$SQUASHFS" | cut -f1)"

# ── GRUB Safety Net: Force Vaelix Identity ──────────────────────────────────
log "Applying v1.1 GRUB Safety Net..."
echo "1978" | sudo -S sed -i 's/boot=casper/boot=casper username=vaelix user-fullname=vaelix/g' "$ISO_DIR/boot/grub/grub.cfg"
ok "GRUB configuration synchronized with Vaelix identity."

# ── Build final ISO with xorriso ─────────────────────────────────────────────
log "Building Vaelix-1.1-QuantumEdge.iso with xorriso..."
echo "1978" | sudo -S rm -f "$ISO_OUT"

echo "1978" | sudo -S xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "VAELIX_OS_1_1" \
    -volset "Vaelix OS 1.1 Quantum" \
    -publisher "Vaelix OS Project" \
    -preparer "Vaelix Build System" \
    -appid "Vaelix OS 1.1 Live" \
    -eltorito-boot boot/grub/i386-pc/eltorito.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --grub2-boot-info \
    --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    --protective-msdos-label \
    -output "$ISO_OUT" \
    "$ISO_DIR" \
    2>&1 | grep -vE "^(xorriso : UPDATE|xorriso : NOTE.*blocks)" | head -30

ISO_SIZE=$(du -sh "$ISO_OUT" 2>/dev/null | cut -f1 || echo "?")
ok "═══════════════════════════════════════"
ok " Vaelix OS 1.1 ISO created!"
ok " Path: $ISO_OUT"
ok " Size: $ISO_SIZE"
ok "═══════════════════════════════════════"
echo ""
echo "  Release: v1.1 Quantum Edge (Production Stable)"
echo "  md5sum: $(md5sum "$ISO_OUT" | cut -d' ' -f1)"
