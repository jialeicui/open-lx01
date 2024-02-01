TOP_DIR ?= $(PWD)/../..
include $(TOP_DIR)/scripts/config.mk

define copy_to_rootfs
	install -d $(DEST_ROOTFS)/usr/bin
	install -m 0755 aivs-monitor $(DEST_ROOTFS)/usr/bin
	# copy json-c lib (curl exist in lx01 rootfs)
	install -d $(DEST_ROOTFS)/usr/lib
	install -m 0755 $(EXTRA_LIB_DIR)/libjson-c.so.5 $(DEST_ROOTFS)/usr/lib
endef

.PHONY: build build-curl build-with-docker build-all

build-with-docker:
	docker run --rm -v $(TOP_DIR):/build -w /build $(BUILD_IMAGE) sh -c "cd $(MAKEFILE_DIR) && make build"

build:
	${CC} -Os -ldl \
		-I $(EXTRA_INCLUDE_DIR) \
		-L $(EXTRA_LIB_DIR) \
		-lcurl \
		-ljson-c \
		-o aivs-monitor \
		json.c \
		main.c
	$(copy_to_rootfs)

lint:
	cppcheck --std=c99 --language=c --error-exitcode=1 --suppress=missingIncludeSystem .

