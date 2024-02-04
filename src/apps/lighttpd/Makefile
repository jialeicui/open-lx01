TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk
include $(TOP_DIR)/scripts/build.mk

SOURCE_CODE_URL ?= "https://git.lighttpd.net/lighttpd/lighttpd1.4/archive/master.tar.gz"

# note that the --prefix when configuring must be /usr/ and not $(PREFIX) because the lighttpd binary is hardcoded to look for the modules in the `--prefix` path
# so we must manually copy the binary and the module to the $(PREFIX) path
define build
	export PKG_CONFIG_PATH=$(DESTDIR)/lib/pkgconfig:$(PKG_CONFIG_PATH) && \
	cd $(PKG_BUILD_DIR) && \
	export LUA_CFLAGS="-I$(EXTRA_INCLUDE_DIR)" && \
	export LUA_LIBS="-L$(EXTRA_LIB_DIR) -llua" && \
	./autogen.sh && \
    ./configure --build=arm-linux --host=$(HOST) --prefix=/data/ --disable-static --enable-shared --without-pcre2 --without-zlib --with-lua && \
	make -j$(nproc) && \
	make install DESTDIR=$(DESTDIR) && \
	cp -v src/lighttpd $(DESTDIR)/bin/lighttpd && \
	cp -v src/.libs/*.so $(DESTDIR)/lib/ && \
	$(copy_to_rootfs)
endef


define copy_to_rootfs
	install -d $(DEST_ROOTFS)/usr/bin && \
	install -m 0755 $(DESTDIR)/bin/lighttpd $(DEST_ROOTFS)/usr/bin && \
	install -d $(DEST_ROOTFS)/usr/lib && \
	install -m 0755 $(DESTDIR)/lib/mod_magnet.so $(DEST_ROOTFS)/usr/lib
endef
