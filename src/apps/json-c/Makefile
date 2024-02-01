TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk
include $(TOP_DIR)/scripts/build.mk

SOURCE_CODE_URL ?= "https://github.com/json-c/json-c/archive/json-c-0.17-20230812.tar.gz"
MD5SUM ?= 6d724389b0a08c519d9dd6e2fac7efb8

define build
	cd $(PKG_BUILD_DIR) && \
	cmake -DCMAKE_INSTALL_PREFIX=$(PREFIX) . && \
	make -j$(nproc) && \
	make install DESTDIR=$(DESTDIR)
endef

