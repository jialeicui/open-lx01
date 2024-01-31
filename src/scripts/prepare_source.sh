#!/bin/bash

set -e
set -x

NAME="$1"
URL="$2"
DEST_DIR="$3"
BUILD_DIR="$4"
MD5SUM="$5" # optional

if [ -z "$NAME" ] || [ -z "$URL" ] || [ -z "$DEST_DIR" ] || [ -z "$BUILD_DIR" ]; then
    echo "Usage: $0 <name> <url> <dest_dir> <build_dir>"
    exit 1
fi

FILE_NAME="${DEST_DIR}/${NAME}/$(basename "${URL}")"

# ensure the destination directory exists
mkdir -pv "${DEST_DIR}/${NAME}"
mkdir -pv "${BUILD_DIR}/${NAME}"

# check if the source exists and the md5sum matches, remove the source if it doesn't
if [ -f "${FILE_NAME}" ]; then
    if [ -n "$MD5SUM" ]; then
        if [ "$(md5sum "${FILE_NAME}" | cut -d' ' -f1)" != "$MD5SUM" ]; then
            rm -v "${FILE_NAME}"
        fi
    fi
fi

# check if the source is already downloaded
if [ ! -f "${FILE_NAME}" ]; then
    # download the source
    wget -O "${FILE_NAME}" "${URL}"
fi

# extract the source
tar -xvf "${FILE_NAME}" -C "${BUILD_DIR}/${NAME}" --strip-components=1
