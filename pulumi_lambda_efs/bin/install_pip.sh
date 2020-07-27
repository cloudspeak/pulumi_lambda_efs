
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [efs_filesystem_id]"
    exit 1
fi

EFS_ID=$1

EFS_PIP_PREFIX=/lambda_packages/pip
LOCAL_PIP_PREFIX=/mnt/efs${EFS_PIP_PREFIX}
DOCKER_PIP_PREFIX=/pip

EFS_PIP_CACHE_PREFIX=/lambda_packages/pip_cache
LOCAL_PIP_CACHE_PREFIX=/mnt/efs${EFS_PIP_CACHE_PREFIX}
DOCKER_PIP_CACHE_PREFIX=/pip_cache

mkdir -p ${LOCAL_PIP_PREFIX}
mkdir -p ${LOCAL_PIP_CACHE_PREFIX}

SCRIPT="

if [ ! -f /inputdir/requirements.txt ]; then
  echo 'ERROR: Cannot find requirements.txt in local directory';
  exit 1;
fi;

echo 'Invoking pip...'
pip install --target ${DOCKER_PIP_PREFIX} -r /inputdir/requirements.txt --cache-dir=${DOCKER_PIP_CACHE_PREFIX}

echo 'Done.';
"

echo "Launching Docker...";

# Run docker to install contents of brewfile
docker run \
    -v $(pwd):/inputdir \
    -v ${LOCAL_PIP_PREFIX}:${DOCKER_PIP_PREFIX} \
    -v ${LOCAL_PIP_CACHE_PREFIX}:${DOCKER_PIP_CACHE_PREFIX} \
    lambci/lambda:build-python3.7 bash -c "${SCRIPT}" \
    || exit 1
