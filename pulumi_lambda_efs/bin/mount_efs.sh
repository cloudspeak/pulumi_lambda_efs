#!/bin/sh

# This script mounts the EFS filesystem with the given ID to /mnt/efs.
# The mount driver will be installed using yum if not already present.
#
# This script is designed to be used on an Amazon EC2 instance, but should work
# on any machine with access to the EFS and with yum installed.
#
# Usage: mount_efs.sh [efs_filesystem_id]

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [efs_filesystem_id]"
    exit 1
fi

EFS_ID=$1
MOUNT_PATH=/mnt/efs

# If EFS has not yet been mounted, mount it

if ! mount | grep -q "$EFS_ID"; then
    echo "Mounting EFS $EFS_ID into ${MOUNT_PATH}...";
    sudo yum install -q -y amazon-efs-utils || exit 1;
    sudo mkdir -p ${MOUNT_PATH} || exit 1;
    sudo mount -t efs $EFS_ID:/ ${MOUNT_PATH} || exit 1;

    if [ ! $? -eq 0 ]; then
        echo "Failed to mount EFS"
        exit 1
    fi

    sudo mkdir -p ${MOUNT_PATH}/lambda_packages || exit 1;
    echo "Mounted successfully.";
fi
