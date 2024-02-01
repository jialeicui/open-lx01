BUILD_IMAGE ?= lx01:latest
NAME=$(shell basename $(shell pwd))

MAKEFILE_DIR=apps/$(NAME)

WORKDIR=$(TOP_DIR)/tmp
DESTDIR=$(WORKDIR)/dists
PKG_BUILD_DIR=$(WORKDIR)/build/$(NAME)
BUILD_STATUS_FILE=$(PKG_BUILD_DIR)/.open-lx01-build-status

EXTRA_INCLUDE_DIR=$(DESTDIR)/include
EXTRA_LIB_DIR=$(DESTDIR)/lib

DEST_ROOTFS=$(WORKDIR)/rootfs

CFLAGS += -I$(EXTRA_INCLUDE_DIR)
LDFLAGS += -L$(EXTRA_LIB_DIR)

# dir tree
# .
# ├── tmp
# │   ├── build
# │   ├── download
# │   ├── rootfs
# │   └── dists
# ├── apps
# │   ├── curl
# │   ├── lighttpd
# │   └── json-c
# ├── scripts
# │   ├── config.mk
# │   ├── prepare_source.sh
# │   └── build.sh
# ├── pack
# └── cross-build-env


define dir_name
	$(shell basename $(shell pwd))
endef

define prepare_source
	(mkdir -pv $(WORKDIR)/download && \
	mkdir -pv $(WORKDIR)/build && \
	mkdir -pv $(WORKDIR)/rootfs && \
	mkdir -pv $(WORKDIR)/dists && \
	$(TOP_DIR)/scripts/prepare_source.sh $(NAME) $(SOURCE_CODE_URL) $(WORKDIR)/download $(WORKDIR)/build)
endef

define mark_build_success
	(echo "build success" && \
	echo $(SOURCE_CODE_URL) > $(BUILD_STATUS_FILE))
endef

define built_success
	(echo $(SOURCE_CODE_URL) | diff -q $(BUILD_STATUS_FILE) - > /dev/null 2>&1)
endef

define build_wrapper
	(if [ -f $(BUILD_STATUS_FILE) ]; then \
		$(built_success) || $(prepare_source) && $(build); \
	else \
		$(prepare_source) && $(build) && $(mark_build_success); \
	fi)
endef

define build_with_docker
	(docker run --rm -v $(TOP_DIR):/build -w /build $(BUILD_IMAGE) sh -c "cd $(MAKEFILE_DIR) && make build")
endef
