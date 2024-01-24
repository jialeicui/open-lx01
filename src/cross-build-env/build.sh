#!/bin/bash

set -e

curl -L https://codeload.github.com/richfelker/musl-cross-make/zip/refs/heads/master -o musl-cross-make.zip

unzip musl-cross-make.zip

pushd musl-cross-make-master
# create config.mak

cat << EOF > config.mak
TARGET = armv7l-linux-musleabihf
OUTPUT = /opt/cross
MUSL_VER = 1.1.14

GCC_CONFIG += --with-arch=armv7-a --with-float=hard --with-fpu=vfpv3

EOF

make -j$(nproc)
make install

popd

