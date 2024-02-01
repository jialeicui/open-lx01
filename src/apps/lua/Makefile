TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk
include $(TOP_DIR)/scripts/build.mk

SOURCE_CODE_URL ?= "https://www.lua.org/ftp/lua-5.1.5.tar.gz"
PATCHE=$(PWD)/01.patch

define build
	cd $(PKG_BUILD_DIR) && \
	patch -p1 < $(PATCHE) && \
	make -j$(nproc) CFLAGS="$(CFLAGS)" CC=$(CC) MYLDFLAGS="$(LDFLAGS)" PKG_VERSION="5.1.5" linux && \
	make install INSTALL_TOP=$(DESTDIR)/$(PREFIX)
endef

