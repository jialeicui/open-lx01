DOWNLOAD_URL ?= "https://git.lighttpd.net/lighttpd/lighttpd1.4/archive/master.tar.gz"
PREFIX ?=
DESTDIR ?= $(PWD)/../dists
DOCKER_IMAGE ?= lx01:latest

NAME=$(shell basename $(shell pwd))

.PHONY: build build-in-docker

build-with-docker:
	docker run --rm -v $(PWD)/../:/build -w /build $(DOCKER_IMAGE) sh -c "cd $(NAME) && make build"

# note that the --prefix when configuring must be /usr/ and not $(PREFIX) because the lighttpd binary is hardcoded to look for the modules in the `--prefix` path
# so we must manually copy the binary and the module to the $(PREFIX) path
build:
	export PKG_CONFIG_PATH=$(DESTDIR)/lib/pkgconfig:$PKG_CONFIG_PATH \
	&& rm -rf ../build/$(NAME) && mkdir -pv ../build/$(NAME) && cd ../build \
	&& wget -c $(DOWNLOAD_URL) -O $(NAME).tar.gz \
	&& tar -xvf $(NAME).tar.gz -C $(NAME) --strip-components=1 \
	&& cd $(NAME) \
	&& export LUA_CFLAGS="-I /build/dists/include" \
	&& export LUA_LIBS="$(LDFLAGS) -llua" \
	&& ./autogen.sh \
    && ./configure --build=arm-linux --host=$(HOST) --prefix=/usr/ --disable-static --enable-shared --without-pcre2 --without-zlib --with-lua \
	&& make -j$(nproc) \
	&& make install DESTDIR=$(DESTDIR) \
	&& cp -v src/lighttpd $(DESTDIR)/bin/lighttpd \
	&& cp -v src/.libs/mod_magnet.so $(DESTDIR)/lib/

