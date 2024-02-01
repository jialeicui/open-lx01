TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk
include $(TOP_DIR)/scripts/build.mk

SOURCE_CODE_URL ?= "https://ftp.gnu.org/gnu/ncurses/ncurses-6.4.tar.gz"

define build
	cd $(PKG_BUILD_DIR) && \
	./configure --prefix=$(PREFIX) --host=$(HOST) && \
	make -j$(nproc) && \
	make install DESTDIR=$(DESTDIR)
endef

