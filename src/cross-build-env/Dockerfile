FROM ubuntu:20.04

ENV TZ=Asia/Shanghai


RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
	&& apt-get update \
	&& apt-get install -y make curl unzip wget xz-utils patch \
		gcc g++ \
	&& apt-get clean all \
	&& rm -rf /var/lib/apt/lists/* /tmp* /var/tmp/*

COPY build.sh /build.sh

RUN mkdir /build
WORKDIR /build

ARG HTTPS_PROXY
RUN chmod +x /build.sh && https_proxy=${HTTPS_PROXY} /build.sh && rm -rf /build.sh && rm -rf /build

ENV CC=/opt/cross/bin/armv7l-linux-musleabihf-cc
ENV CXX=/opt/cross/bin/armv7l-linux-musleabihf-g++
ENV AR=/opt/cross/bin/armv7l-linux-musleabihf-ar
ENV RANLIB=/opt/cross/bin/armv7l-linux-musleabihf-ranlib
ENV STRIP=/opt/cross/bin/armv7l-linux-musleabihf-strip
ENV LD=/opt/cross/bin/armv7l-linux-musleabihf-ld
ENV AS=/opt/cross/bin/armv7l-linux-musleabihf-as
ENV PATH=/opt/cross/bin:$PATH
ENV HOST=armv7l-linux-musleabihf
ENV CFLAGS="-O2 -pipe -fPIC -fstack-protector-strong -fno-plt -march=armv7-a -mfloat-abi=hard -mfpu=neon -mtune=cortex-a7"
