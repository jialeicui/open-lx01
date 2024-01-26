DOWNLOAD_URL ?= "https://github.com/openwrt/libubox/archive/master.tar.gz"
PREFIX ?= 
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

NAME=$(shell basename $(shell pwd))

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd $(NAME) && make build"

build:
	export PKG_CONFIG_PATH=$(DESTDIR)/lib/pkgconfig:$PKG_CONFIG_PATH && \
	rm -rf ../build/$(NAME) && mkdir -pv ../build/$(NAME) && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O $(NAME).tar.gz \
	&& tar -xvf $(NAME).tar.gz -C $(NAME) --strip-components=1 \
	&& cd $(NAME) \
	&& cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) -DBUILD_EXAMPLES=OFF -DBUILD_LUA=OFF . \
	&& make -j$(nproc) \
	&& make install DESTDIR=$(DESTDIR) \
	&& cd ../ && rm -rf $NAME
