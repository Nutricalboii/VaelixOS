#!/bin/bash
# Vaelix OS — Phase 13: Resurrection & Recovery
# Implementation of Timeshift snapshots and the vx restore mechanism.

set -e

CHROOT_DIR="$(pwd)/build/mnt"

# Helper to run commands inside chroot
run_chroot_raw() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "$1"
}

run_chroot() {
    echo "1978" | sudo -S chroot "${CHROOT_DIR}" /bin/bash -c "eatmydata $1"
}

echo "✦ Phase 13: Forging the Vaelix Safety Net..."

# 1. Install Timeshift
echo "✦ Installing Timeshift for system snapshots..."
run_chroot "apt install -y timeshift"

# 2. Configure default Timeshift settings (RSYNC for broad compatibility)
# We set a basic schedule: Daily (2 kept), Weekly (1 kept)
run_chroot_raw "mkdir -p /etc/timeshift
cat <<EOF > /etc/timeshift/timeshift.json
{
  \"backup_device_uuid\": \"\",
  \"parent_device_uuid\": \"\",
  \"do_first_run\": \"false\",
  \"btrfs_mode\": \"false\",
  \"include_btrfs_home_for_backup\": \"false\",
  \"include_btrfs_home_for_restore\": \"false\",
  \"stop_cron_emails\": \"true\",
  \"btrfs_use_qgroup\": \"true\",
  \"schedule_monthly\": \"false\",
  \"schedule_weekly\": \"true\",
  \"schedule_daily\": \"true\",
  \"schedule_hourly\": \"false\",
  \"schedule_boot\": \"false\",
  \"count_monthly\": \"2\",
  \"count_weekly\": \"3\",
  \"count_daily\": \"5\",
  \"count_hourly\": \"6\",
  \"count_boot\": \"5\",
  \"snapshot_size\": \"0\",
  \"snapshot_count\": \"0\",
  \"exclude\": [
    \"/home/vaelix/**\",
    \"/root/**\"
  ],
  \"include\": []
}
EOF"

echo "✦ Vaelix OS: Resurrection Layer (Timeshift) Applied."
