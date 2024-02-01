export TOP_DIR ?= $(abspath $(PWD)/..)
include $(TOP_DIR)/scripts/config.mk

.PHONY: all copy_to_rootfs

# TODO support dependency auto build
all:
	for app in ncurses readline curl json-c lua lighttpd aivs-monitor; do \
		$(MAKE) -C $$app; \
	done
