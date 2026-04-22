#!/bin/bash
# Vaelix OS — Phase 5: ISO Builder
# Produces a bootable Vaelix-1.0.iso from the rootfs image
set -e

WORK="$(pwd)/build"
MNT="${WORK}/mnt"
ISO_DIR="${WORK}/iso"
ISO_OUT="${WORK}/Vaelix-1.0.iso"
KERNEL_VER="$(ls ${MNT}/boot/vmlinuz-* 2>/dev/null | sort -V | tail -1 | xargs -I{} basename {} | sed 's/vmlinuz-//')"
KERNEL_VER="${KERNEL_VER:-$(uname -r)}"

log() { echo -e "\e[35m✦\e[0m $*"; }
ok()  { echo -e "\e[32m✅\e[0m $*"; }

log "Starting Vaelix ISO build..."
log "Kernel detected: ${KERNEL_VER}"

# ─── Step 1: Create ISO directory structure ───────────────────────────────────
log "Step 1: Building ISO directory tree..."
echo "1978" | sudo -S rm -rf "${ISO_DIR}"
echo "1978" | sudo -S mkdir -p \
    "${ISO_DIR}/boot/grub" \
    "${ISO_DIR}/live" \
    "${ISO_DIR}/.disk"

# ─── Step 2: Copy kernel and initrd ──────────────────────────────────────────
log "Step 2: Copying kernel and initrd..."
VMLINUZ=$(ls "${MNT}/boot/vmlinuz-"* 2>/dev/null | sort -V | tail -1)
INITRD=$(ls  "${MNT}/boot/initrd.img-"* 2>/dev/null | sort -V | tail -1)

if [ -z "$VMLINUZ" ]; then
    # Fall back to the running kernel's vmlinuz
    VMLINUZ="/boot/vmlinuz-$(uname -r)"
    INITRD="/boot/initrd.img-$(uname -r)"
    log "Warning: using host kernel as fallback"
fi

echo "1978" | sudo -S cp "$VMLINUZ" "${ISO_DIR}/boot/vmlinuz"
echo "1978" | sudo -S cp "$INITRD"  "${ISO_DIR}/boot/initrd.img"
ok "Kernel: $(basename $VMLINUZ)"

# ─── Step 3: Build squashfs ──────────────────────────────────────────────────
log "Step 3: Building squashfs filesystem (this takes a while)..."
echo "1978" | sudo -S apt install -y squashfs-tools xorriso grub-efi-amd64-bin grub-pc-bin 2>&1 | grep -E "^(Get:|The follow|Unpack|Setting)" | head -5

echo "1978" | sudo -S mksquashfs "${MNT}" "${ISO_DIR}/live/filesystem.squashfs" \
    -e boot \
    -comp zstd -Xcompression-level 9 \
    -noappend \
    -info \
    -wildcards \
    -ef <(cat << 'EXCLUDES'
proc/*
sys/*
dev/*
tmp/*
var/cache/apt/archives/*.deb
var/log/*.log
root/.bash_history
home/*/.bash_history
EXCLUDES
)

ok "Squashfs: $(du -sh ${ISO_DIR}/live/filesystem.squashfs | cut -f1)"

# ─── Step 4: GRUB config ─────────────────────────────────────────────────────
log "Step 4: Writing GRUB bootloader config..."
cat > /tmp/vaelix_grub.cfg << 'GRUB'
set default=0
set timeout=5
set timeout_style=countdown

# Vaelix OS branding
set menu_color_normal=black/black
set menu_color_highlight=white/black

insmod all_video
insmod gfxterm
insmod gfxmenu
terminal_output gfxterm

menuentry "Vaelix OS 1.0  ·  Live Session" --class vaelix --class os {
    linux  /boot/vmlinuz boot=live quiet splash rw
    initrd /boot/initrd.img
}

menuentry "Vaelix OS 1.0  ·  Install" --class vaelix --class os {
    linux  /boot/vmlinuz boot=live quiet splash rw installer
    initrd /boot/initrd.img
}

menuentry "Vaelix OS 1.0  ·  Safe Mode" --class vaelix --class os {
    linux  /boot/vmlinuz boot=live nomodeset
    initrd /boot/initrd.img
}

menuentry "Firmware Setup (UEFI)" --class efi {
    fwsetup
}
GRUB

echo "1978" | sudo -S cp /tmp/vaelix_grub.cfg "${ISO_DIR}/boot/grub/grub.cfg"

# Disk info file
echo "Vaelix OS 1.0 — Built $(date +%Y-%m-%d)" | \
    echo "1978" | sudo -S tee "${ISO_DIR}/.disk/info" > /dev/null
echo "1978" | sudo -S touch "${ISO_DIR}/.disk/base_installable"

# ─── Step 5: Build ISO ───────────────────────────────────────────────────────
log "Step 5: Generating bootable ISO with xorriso..."

echo "1978" | sudo -S xorriso -as mkisofs \
    -o "${ISO_OUT}" \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "VAELIX_OS_1_0" \
    -b boot/grub/i386-pc/eltorito.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --grub2-boot-info \
    --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    --protective-mbd \
    -graft-points \
        "${ISO_DIR}/=/" \
        "boot/grub/i386-pc/eltorito.img=/usr/lib/grub/i386-pc/cdboot.img" \
    2>&1 | grep -E "^(xorriso|Total|Written|ISO)" | head -20 || \
# Simplified fallback if grub hybrid boot fails
echo "1978" | sudo -S xorriso -as mkisofs \
    -o "${ISO_OUT}" \
    -iso-level 3 \
    -volid "VAELIX_OS_1_0" \
    -R -J \
    "${ISO_DIR}/"

ISO_SIZE=$(du -sh "${ISO_OUT}" 2>/dev/null | cut -f1 || echo "?")
ok "ISO created: ${ISO_OUT} (${ISO_SIZE})"
ok "Vaelix OS 1.0 is ready."
echo ""
echo "  Write to USB:  sudo dd if=${ISO_OUT} of=/dev/sdX bs=4M status=progress"
echo "  Or use:        balenaEtcher / Ventoy"
