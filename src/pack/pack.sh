#!/bin/bash

set -e

BASE_DIR=`pwd`
WORK_DIR=`pwd`/tmp
#MD5SUM="1ae7eb1bdbb764b946654a08dfec1cac"
URL="https://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/lx01/mico_firmware_c1cac_1.56.1.bin"

# if firmware.bin exists, skip download
if [ -f mico_firmware_c1cac_1.56.1.bin ]; then
	echo "firmware.bin exists, skip download"
else
	wget -c $URL
fi

rm -rf $WORK_DIR && mkdir -pv $WORK_DIR && ln -sf $BASE_DIR/mico_firmware_c1cac_1.56.1.bin $WORK_DIR/firmware.bin
pushd $WORK_DIR

dd if=firmware.bin bs=8 skip=524409 of=rootfs.img
unsquashfs rootfs.img && rm -rf rootfs.img

pushd squashfs-root

PATCH_DIR=$BASE_DIR/patches
PATCHES=`ls $PATCH_DIR/*.patch | sort -n`

for patch in $PATCHES; do
	patch -p1 < $patch
done

popd

mksquashfs squashfs-root rootfs.img -comp xz -b 256K -noappend && mv rootfs.img $BASE_DIR/rootfs.img

popd

rm -rf $WORK_DIR

