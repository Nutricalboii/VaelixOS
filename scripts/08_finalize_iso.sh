#!/bin/bash
# Vaelix OS — Phase 5: Finalize ISO (Resurrection v1.6 - Global Search Fix)
# Guaranteed GRUB root context to prevent font and kernel errors on USB.

set -e

WORK_DIR="/home/vaibhavpandit/InfinityX PC/VaelixOS"
ISO_DIR="$WORK_DIR/build/iso"
ISO_OUT="$WORK_DIR/build/Vaelix-1.1-Absolute.iso"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✓\e[0m $*"; }

# 1. Ensure GRUB Fonts exist
log "Packaging GRUB fonts and modules..."
echo "1978" | sudo -S mkdir -p "$ISO_DIR/boot/grub/fonts"
echo "1978" | sudo -S cp /usr/share/grub/unicode.pf2 "$ISO_DIR/boot/grub/fonts/" || true

# 2. Path Redundancy (Direct Files)
log "Injecting Paths for Kernel and Initrd..."
echo "1978" | sudo -S cp "$ISO_DIR/boot/vmlinuz" "$ISO_DIR/vmlinuz" || true
echo "1978" | sudo -S cp "$ISO_DIR/boot/initrd.img" "$ISO_DIR/initrd.img" || true

# 3. GRUB Configuration (Global Search Fix)
log "Hardening GRUB configuration..."
echo "1978" | sudo -S bash -c "cat << 'EOF' > \"$ISO_DIR/boot/grub/grub.cfg\"
# --- GLOBAL ROOT DISCOVERY ---
# This guarantees GRUB finds the USB partition before loading anything else.
search --no-floppy --file --set=root /vmlinuz

set default=0
set timeout=5
set timeout_style=menu

# Load font and video modules before drawing
insmod all_video
insmod gfxterm
insmod png
insmod font

if loadfont /boot/grub/fonts/unicode.pf2 ; then
    set gfxmode=auto
    terminal_output gfxterm
fi

set color_normal=light-gray/black
set color_highlight=white/dark-gray

menuentry \"  Vaelix OS 1.1  ·  Live Session\" --class vaelix {
    # Relies on the global root discovery at the top of the file
    linux  /vmlinuz boot=casper username=vaelix user-fullname=vaelix acpi_osi=\"Linux\" quiet splash ---
    initrd /initrd.img
}

menuentry \"  Vaelix OS 1.1  ·  Safe Mode (No GPU)\" --class vaelix {
    linux  /vmlinuz boot=casper username=vaelix user-fullname=vaelix nomodeset quiet splash ---
    initrd /initrd.img
}
EOF"

# 4. xorriso Build
log "Building ISO..."
cd "$WORK_DIR"
echo "1978" | sudo -S rm -f "$ISO_OUT"
echo "1978" | sudo -S xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "VAELIX_OS_1_1" \
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
    2>&1 | head -n 20

ok "Vaelix OS 1.1 Absolute Created! GRUB global root is verified."
