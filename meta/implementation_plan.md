# InfinityOS Implementation Plan

InfinityOS is designed to be a premium, lightweight, and performance-optimized Linux distribution based on Ubuntu, featuring a custom KDE Plasma experience and deep hardware integration for gaming laptops.

## User Review Required

> [!IMPORTANT]
> **GitHub Repository**: I will initialize a GitHub repository for InfinityOS to track all scripts, themes, and configurations.
> **Base OS Choice**: I have selected **Ubuntu 24.04 LTS** (or latest stable) as the base.
> **Development Isolation**: All builds will occur in `~/InfinityOS` and be tested via **QEMU/KVM**.
> **NVIDIA Support**: Latest proprietary drivers (550+) will be pre-installed.
> **Testing Strategy**: We will use your **320GB HDD enclosure** for real hardware testing of the Live ISO.

## Phase 0: GitHub Repository Initialization [NEW]
- Create local git repo in `~/InfinityOS`.
- Set up `.gitignore` for build artifacts and large ISO files.
- Push initial structure and implementation plan.

## Phase 1: Research Findings (Summary)

Based on the initial deep research, here are the benchmarks and targets for InfinityOS:

| Metric | Target | Method |
| :--- | :--- | :--- |
| **Idle RAM** | < 1.2 GB | Stripped KDE Plasma + minimal background services. |
| **Boot Time** | < 12 seconds | systemd prunning + optimized initramfs. |
| **Battery Life** | +25% vs Stock | TLP + power-profiles-daemon + auto-cpufreq. |
| **Gaming** | Parity with Windows | XanMod Kernel + MESA/NVIDIA optimizations + Gamemode. |
| **UI/UX** | Premium/Futuristic | Custom Blur/Glassmorphism + Dynamic Accent Colors. |

## Proposed Execution Phases

### Phase 2: Build Environment & Base Setup [NEW]
- Set up a dedicated workspace: `~/InfinityOS`.
- Create building scripts using `debootstrap` for a clean, bloat-free base.
- configure APT mirrors and basic repository structure.

### Phase 3: Performance & Kernel Engineering [NEW]
- Integrate **XanMod** or **Liquirix** kernel for reduced latency.
- Implement `zram-tools` for better memory management.
- Configure `systemd` service optimizations.

### Phase 4: Visual Identity & "macOS 26" UI [MODIFY]
- **Theme Engine**: Install `kvantum` for advanced glassmorphism application styles.
- **Desktop**: Install `plasma-desktop` (minimal) and `sddm`.
- **Global Theme**: Implement a custom "Neo-Luxe" theme based on **Orchis** and **WhiteSur** DNA.
- **Window Management**: Use **Klassy** for rounded corners, thin borders, and centered titles.
- **Typography**: Configure **Inter** for UI, **JetBrains Mono** for terminal.
- **Animations**: Tune KWin effects to **200ms** for that "expensive" motion feel.
- **Dock/Panel**: Centered top-bar with system tray and a floating dock at the bottom.

### Phase 5: Infinity Control Center [NEW]
- Develop a Python/PyQt6 application for system management.
- Modules: Performance profiles (Beast/Eco), GPU Switcher, RGB Sync, and AI Troubleshooter.

### Phase 6: ISO Mastering & Pipeline [NEW]
- Use `xorriso` and `squashfs-tools` to generate the final bootable ISO.
- Implement a Calamares-based installer with custom branding.

## Open Questions

1. **Kernel Preference**: Do you prefer a stable LTS kernel or a high-performance rolling kernel (XanMod/Liquirix)?
2. **AI Integration**: Should the "Control Center" include a built-in terminal-based AI assistant (like a specialized version of me) for system troubleshooting?
3. **App Selection**: Should we include Flatpak support by default, or stick to native APT to keep the image slim?

## Verification & Hardware Testing [NEW]

### Automated Tests
- `qemu-system-x86_64` scripts to boot the ISO.
- RAM usage benchmarks (Target: < 1.2GB idle).

### Manual & Real Hardware Testing
1. **HDD Enclosure Testing**: We will use `dd` or `Etcher-cli` to burn the generated ISO to your **320GB HDD**.
2. **Boot Test**: Boot from the HDD on your LOQ to verify:
    - Wi-Fi/Bluetooth hardware detection.
    - NVIDIA Prime switching (Intel/NVIDIA GPU).
    - Thermal and Fan profiles.
    - Trackpad gestures (macOS style).
