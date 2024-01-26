DOWNLOAD_URL ?= "https://www.lua.org/ftp/lua-5.1.5.tar.gz"
PREFIX ?= 
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

NAME=$(shell basename $(shell pwd))
PATCHE=$(PWD)/01.patch

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd $(NAME) && make build"

build:
	rm -rf ../build/$(NAME) && mkdir -pv ../build/$(NAME) && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O $(NAME).tar.gz \
	&& tar -xvf $(NAME).tar.gz -C $(NAME) --strip-components=1 \
	&& cd $(NAME) \
	&& patch -p1 < $(PATCHE) \
	&& make -j$(nproc) CFLAGS="$(CFLAGS)" CC=$(CC) MYLDFLAGS="$(LDFLAGS)" PKG_VERSION="5.1.5" linux \
	&& make install INSTALL_TOP=$(DESTDIR)/$(PREFIX)

