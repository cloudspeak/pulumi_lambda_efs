#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [efs_filesystem_id]"
    exit 1
fi

EFS_ID=$1
EFS_BREW_PREFIX=/lambda_packages/linuxbrew
LOCAL_BREW_PREFIX=/mnt/efs${EFS_BREW_PREFIX}

if [ ! -d ${LOCAL_BREW_PREFIX}/Homebrew ]; then
    echo "Initializing Linuxbrew prefix into ${LOCAL_BREW_PREFIX}..."
    sudo mkdir -p ${LOCAL_BREW_PREFIX} || exit 1
    sudo docker run \
        -v ${LOCAL_BREW_PREFIX}:/newprefix \
        nuagestudio/amazonlinuxbrew bash -c "sudo cp -a /home/linuxbrew/.linuxbrew/* /newprefix" \
        || exit 1
fi;



DOCKER_BREW_PREFIX="/home/linuxbrew/.linuxbrew"


SCRIPT="

if [ ! -f /inputdir/Brewfile ]; then
  echo 'ERROR: Cannot find Brewfile in local directory';
  exit 1;
fi;

if [ ! -f ${DOCKER_BREW_PREFIX}/bin/ld ] || [ ! -f ${DOCKER_BREW_PREFIX}/bin/objdump ]; then
    echo 'Installing objdump and ld...';
    sudo yum install -y yum-utils rpmdevtools;
    sudo yumdownloader --resolve binutils;
    rpmdev-extract *.rpm;
    sudo cp -P -R ./binutils*/usr/lib64/* ${DOCKER_BREW_PREFIX}/lib;
    sudo cp -P ./binutils*/usr/bin/ld.bfd ${DOCKER_BREW_PREFIX}/bin/ld;
    sudo cp -P ./binutils*/usr/bin/objdump ${DOCKER_BREW_PREFIX}/bin;
    sudo rm -rf ./binutils;
    sudo chmod +x ${DOCKER_BREW_PREFIX}/bin/ld
fi

echo 'Invoking brew...'
cp /inputdir/Brewfile .;
brew bundle;

echo 'Done.';
"

echo "Launching Docker...";

# Run docker to install contents of brewfile
docker run \
    -v $(pwd):/inputdir \
    -v ${LOCAL_BREW_PREFIX}:${DOCKER_BREW_PREFIX} \
    nuagestudio/amazonlinuxbrew bash -c "${SCRIPT}" \
    || exit 1
