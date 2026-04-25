#!/bin/bash
# Vaelix OS — Phase 6: Productivity & Developer Experience
# Curated apps: Firefox (Default), VSCodium, LibreOffice, and Terminal tools.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 6: Deploying Productivity & Dev Suite..."

# 1. Repositories for "Non-Standard" Essentials
echo "✦ Adding repositories for VSCodium and Firefox Deb..."
run_chroot_raw "
    # VSCodium Key & Repo
    curl -fSsL https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg | gpg --batch --yes --dearmor -o /usr/share/keyrings/vscodium.gpg
    echo 'deb [ signed-by=/usr/share/keyrings/vscodium.gpg ] https://download.vscodium.com/debs vscodium main' > /etc/apt/sources.list.d/vscodium.list

    # Mozilla PPA (for Firefox Deb instead of Snap)
    add-apt-repository -y ppa:mozillateam/ppa
    echo 'Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001' > /etc/apt/preferences.d/mozilla-firefox
"

run_chroot "apt update"

# 2. Core Productivity Applications
echo "✦ Installing LibreOffice, Firefox, and VSCodium..."
run_chroot "apt install -y \
    firefox \
    libreoffice-plasma libreoffice-calc libreoffice-writer \
    codium"

# 3. Premium Terminal Tools
echo "✦ Installing CLI Power Tools..."
run_chroot "apt install -y \
    eza bat btop fzf zoxide"

# 4. Starship Prompt Installation
echo "✦ Injecting Starship Prompt..."
run_chroot "curl -sS https://starship.rs/install.sh | sh -s -- -y"

# 5. Shell Integration (Bash by default)
echo "✦ Configuring Bash with premium defaults..."
run_chroot_raw "cat <<EOF >> /etc/skel/.bashrc

# Vaelix OS Terminal Enhancements
eval \"\$(starship init bash)\"
eval \"\$(zoxide init bash)\"
alias ls='eza --icons'
alias cat='batcat --paging=never'
alias htop='btop'
EOF"

# 6. Starship Minimal Config
run_chroot_raw "mkdir -p /etc/skel/.config
cat <<EOF > /etc/skel/.config/starship.toml
format = \"\$directory\$git_branch\$character\"
add_newline = false

[directory]
style = \"bold purple\"
truncate_to_repo = true

[git_branch]
symbol = \" \"
style = \"bold blue\"

[character]
success_symbol = \"[➜](bold green)\"
error_symbol = \"[➜](bold red)\"
EOF"

echo "✦ Vaelix OS: Productivity & Dev Suite Deployed."
