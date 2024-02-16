TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk
include $(TOP_DIR)/scripts/build.mk

SOURCE_CODE_URL ?= https://github.com/curl/curl/releases/download/curl-7_59_0/curl-7.59.0.tar.gz
MD5SUM ?= 0bc69288b20ae165ff4b7d6d7bbe70d2

define build
	cd $(PKG_BUILD_DIR) && \
	./configure --host=$(HOST) --prefix=$(PREFIX) --without-ssl && \
	make -j$(nproc) && \
	make install DESTDIR=$(DESTDIR)
endef
