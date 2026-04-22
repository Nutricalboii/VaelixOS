#!/bin/bash
# Vaelix OS — Phase 5: Finalize ISO
# Waits for squashfs to complete then builds the bootable dual-mode ISO.
set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
ISO_DIR="$WORK_DIR/build/iso"
ISO_OUT="$WORK_DIR/build/Vaelix-1.0.iso"
SQUASHFS="$ISO_DIR/live/filesystem.squashfs"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }
err() { echo -e "\e[31m✗\e[0m $*"; }

# ── Wait for squashfs to finish ───────────────────────────────────────────────
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

# ── Verify all ISO components are present ─────────────────────────────────────
log "Verifying ISO structure..."
REQUIRED=(
    "$ISO_DIR/boot/vmlinuz"
    "$ISO_DIR/boot/initrd.img"
    "$ISO_DIR/boot/grub/grub.cfg"
    "$ISO_DIR/boot/grub/i386-pc/eltorito.img"
    "$ISO_DIR/boot/grub/efi.img"
    "$ISO_DIR/EFI/BOOT/BOOTX64.EFI"
    "$ISO_DIR/live/filesystem.squashfs"
    "$ISO_DIR/live/filesystem.manifest"
    "$ISO_DIR/.disk/info"
)
for f in "${REQUIRED[@]}"; do
    [ -f "$f" ] && ok "  $f" || { err "  MISSING: $f"; exit 1; }
done

# ── Build final ISO with xorriso (BIOS + UEFI hybrid) ────────────────────────
log "Building Vaelix-1.0.iso with xorriso..."
echo "1978" | sudo -S rm -f "$ISO_OUT"

echo "1978" | sudo -S xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "VAELIX_OS_1_0" \
    -volset "Vaelix OS 1.0" \
    -publisher "Vaelix OS Project" \
    -preparer "Vaelix Build System" \
    -appid "Vaelix OS 1.0 Live" \
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
ok " Vaelix OS 1.0 ISO created!"
ok " Path: $ISO_OUT"
ok " Size: $ISO_SIZE"
ok "═══════════════════════════════════════"
echo ""
echo "  Flash to USB:   sudo dd if=\"$ISO_OUT\" of=/dev/sdX bs=4M status=progress oflag=sync"
echo "  Or use:         balenaEtcher / Ventoy"
echo ""
echo "  md5sum: $(md5sum "$ISO_OUT" | cut -d' ' -f1)"
